"""
Views for Documents app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer
from ideas.permissions import IsSubmitterOrReadOnly


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document model."""
    
    queryset = Document.objects.select_related('idea', 'uploaded_by')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsSubmitterOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['idea', 'virus_scan_status']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'upload':
            return DocumentUploadSerializer
        return DocumentSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def upload(self, request):
        """Upload a file."""
        serializer = DocumentUploadSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            document = serializer.save()
            response_serializer = DocumentSerializer(document)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def download(self, request, pk=None):
        """Download a file."""
        document = self.get_object()
        
        try:
            file_url = document.get_file_url()
            return Response({'url': file_url})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def scan_status(self, request, pk=None):
        """Get virus scan status."""
        document = self.get_object()
        
        return Response({
            'id': str(document.id),
            'status': document.virus_scan_status,
            'result': document.virus_scan_result
        })
