"""
Serializers for Documents app.
"""

from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'idea', 'file_name', 'file_path', 'file_size', 'file_type',
            'uploaded_by', 'uploaded_at', 'virus_scan_status', 'virus_scan_result',
            'file_url'
        ]
        read_only_fields = [
            'id', 'file_path', 'uploaded_at', 'virus_scan_status',
            'virus_scan_result', 'file_url'
        ]
    
    def get_file_url(self, obj):
        """Get file URL."""
        try:
            return obj.get_file_url()
        except Exception:
            return None


class DocumentUploadSerializer(serializers.Serializer):
    """Serializer for file upload."""
    
    file = serializers.FileField(required=True)
    idea_id = serializers.UUIDField(required=True)
    
    def validate_file(self, value):
        """Validate file."""
        from common.utils import validate_file_size, validate_file_type
        
        # Validate file size (10 MB max)
        validate_file_size(value, max_size_mb=10)
        
        # Validate file type
        validate_file_type(value)
        
        return value
    
    def create(self, validated_data):
        """Create document."""
        from ideas.models import Idea
        from common.utils import upload_file_to_s3, sanitize_filename
        from celery_tasks.file_tasks import scan_uploaded_file
        import uuid
        
        file = validated_data['file']
        idea_id = validated_data['idea_id']
        
        # Get idea
        try:
            idea = Idea.objects.get(id=idea_id)
        except Idea.DoesNotExist:
            raise serializers.ValidationError("Idea not found")
        
        # Sanitize filename
        file_name = sanitize_filename(file.name)
        unique_file_name = f"{uuid.uuid4()}_{file_name}"
        
        # Upload file to S3
        file_path = upload_file_to_s3(file, unique_file_name)
        
        # Create document
        document = Document.objects.create(
            idea=idea,
            file_name=file.name,
            file_path=file_path,
            file_size=file.size,
            file_type=file.name.split('.')[-1].lower(),
            uploaded_by=self.context['request'].user,
            virus_scan_status='PENDING'
        )
        
        # Queue virus scan
        scan_uploaded_file.delay(str(document.id))
        
        return document
