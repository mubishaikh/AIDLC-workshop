"""
Views for Ideas app.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Idea, Campaign, Contributor, Document
from .serializers import (
    IdeaListSerializer, IdeaDetailSerializer, IdeaCreateSerializer,
    CampaignSerializer, ContributorSerializer, DocumentSerializer,
    IdeaSubmitSerializer
)
from .permissions import IsSubmitterOrReadOnly, IsContributor


class CampaignViewSet(viewsets.ModelViewSet):
    """ViewSet for Campaign model."""
    
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'start_date']
    ordering = ['-created_at']


class IdeaViewSet(viewsets.ModelViewSet):
    """ViewSet for Idea model."""
    
    queryset = Idea.objects.select_related('submitter', 'campaign').prefetch_related('contributors', 'documents')
    permission_classes = [IsAuthenticated, IsSubmitterOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'expected_impact', 'campaign']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return IdeaListSerializer
        elif self.action == 'create':
            return IdeaCreateSerializer
        elif self.action == 'submit':
            return IdeaSubmitSerializer
        return IdeaDetailSerializer
    
    def get_queryset(self):
        """Filter ideas based on user role."""
        user = self.request.user
        
        # Admins see all ideas
        if user.is_staff:
            return self.queryset
        
        # Users see their own ideas and all submitted ideas
        return self.queryset.filter(
            models.Q(submitter=user) | models.Q(status__in=['SUBMITTED', 'UNDER_EVALUATION', 'EVALUATED', 'RECOGNIZED'])
        )
    
    def perform_create(self, serializer):
        """Create idea with current user as submitter."""
        serializer.save(submitter=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsSubmitterOrReadOnly])
    def submit(self, request, pk=None):
        """Submit a draft idea."""
        idea = self.get_object()
        
        if idea.status != 'DRAFT':
            return Response(
                {'error': 'Only draft ideas can be submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        idea.status = 'SUBMITTED'
        idea.submitted_at = timezone.now()
        idea.save()
        
        serializer = self.get_serializer(idea)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsSubmitterOrReadOnly])
    def add_contributor(self, request, pk=None):
        """Add a contributor to an idea."""
        idea = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        contributor, created = Contributor.objects.get_or_create(
            idea=idea,
            user=user,
            defaults={'role': 'CONTRIBUTOR'}
        )
        
        if not created:
            return Response(
                {'error': 'User is already a contributor'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def contributors(self, request, pk=None):
        """List contributors for an idea."""
        idea = self.get_object()
        contributors = idea.contributors.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def documents(self, request, pk=None):
        """List documents for an idea."""
        idea = self.get_object()
        documents = idea.documents.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_ideas(self, request):
        """Get current user's ideas."""
        ideas = self.queryset.filter(submitter=request.user)
        serializer = self.get_serializer(ideas, many=True)
        return Response(serializer.data)


class ContributorViewSet(viewsets.ModelViewSet):
    """ViewSet for Contributor model."""
    
    queryset = Contributor.objects.select_related('idea', 'user')
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['idea', 'role']


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document model."""
    
    queryset = Document.objects.select_related('idea')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['idea', 'virus_scan_status']
