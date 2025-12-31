"""
Serializers for Ideas app.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Idea, Campaign, Contributor, Document


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for Campaign model."""
    
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'description', 'status', 'start_date', 'end_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer for Contributor model."""
    
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'user_id', 'role', 'added_at']
        read_only_fields = ['id', 'added_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    
    class Meta:
        model = Document
        fields = ['id', 'file_name', 'file_path', 'file_size', 'file_type', 'uploaded_at', 'virus_scan_status']
        read_only_fields = ['id', 'file_path', 'uploaded_at', 'virus_scan_status']


class IdeaListSerializer(serializers.ModelSerializer):
    """Serializer for Idea list view."""
    
    submitter = UserSerializer(read_only=True)
    contributor_count = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Idea
        fields = ['id', 'title', 'expected_impact', 'submitter', 'status', 'created_at', 'contributor_count', 'document_count']
        read_only_fields = ['id', 'created_at']
    
    def get_contributor_count(self, obj):
        return obj.contributors.count()
    
    def get_document_count(self, obj):
        return obj.documents.count()


class IdeaDetailSerializer(serializers.ModelSerializer):
    """Serializer for Idea detail view."""
    
    submitter = UserSerializer(read_only=True)
    contributors = ContributorSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    campaign = CampaignSerializer(read_only=True)
    
    class Meta:
        model = Idea
        fields = [
            'id', 'title', 'description', 'expected_impact', 'submitter', 'campaign',
            'status', 'created_at', 'updated_at', 'submitted_at', 'recognized_at',
            'contributors', 'documents'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'submitted_at', 'recognized_at']


class IdeaCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating ideas."""
    
    campaign_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Idea
        fields = ['title', 'description', 'expected_impact', 'campaign_id']
    
    def validate_title(self, value):
        """Validate title length and content."""
        if not value or len(value) > 200:
            raise serializers.ValidationError("Title must be 1-200 characters")
        return value.strip()
    
    def validate_description(self, value):
        """Validate description length and content."""
        if not value or len(value) > 2000:
            raise serializers.ValidationError("Description must be 1-2000 characters")
        return value.strip()
    
    def validate_expected_impact(self, value):
        """Validate expected impact."""
        if value not in ['HIGH', 'MEDIUM', 'LOW']:
            raise serializers.ValidationError("Invalid impact level")
        return value
    
    def create(self, validated_data):
        """Create idea with submitter as first contributor."""
        campaign_id = validated_data.pop('campaign_id')
        request = self.context.get('request')
        
        # Create idea
        idea = Idea.objects.create(
            submitter=request.user,
            campaign_id=campaign_id,
            **validated_data
        )
        
        # Add submitter as contributor
        Contributor.objects.create(
            idea=idea,
            user=request.user,
            role='SUBMITTER'
        )
        
        return idea


class IdeaSubmitSerializer(serializers.Serializer):
    """Serializer for submitting a draft idea."""
    
    def update(self, instance, validated_data):
        """Submit idea from draft."""
        from django.utils import timezone
        
        if instance.status != 'DRAFT':
            raise serializers.ValidationError("Only draft ideas can be submitted")
        
        instance.status = 'SUBMITTED'
        instance.submitted_at = timezone.now()
        instance.save()
        
        return instance
