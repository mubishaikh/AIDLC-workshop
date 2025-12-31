"""
Tests for Documents app.
"""

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from ideas.models import Idea, Campaign, Contributor
from .models import Document
from datetime import datetime, timedelta


@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def campaign(db):
    """Create test campaign."""
    return Campaign.objects.create(
        name='Test Campaign',
        description='Test campaign description',
        status='ACTIVE',
        start_date=datetime.now().date(),
        end_date=(datetime.now() + timedelta(days=30)).date()
    )


@pytest.fixture
def idea(db, user, campaign):
    """Create test idea."""
    idea = Idea.objects.create(
        title='Test Idea',
        description='Test idea description',
        expected_impact='HIGH',
        submitter=user,
        campaign=campaign,
        status='SUBMITTED'
    )
    Contributor.objects.create(
        idea=idea,
        user=user,
        role='SUBMITTER'
    )
    return idea


@pytest.fixture
def test_file():
    """Create test file."""
    return SimpleUploadedFile(
        "test_document.pdf",
        b"file_content",
        content_type="application/pdf"
    )


class TestDocumentViewSet:
    """Tests for DocumentViewSet."""
    
    def test_upload_file(self, api_client, user, idea, test_file):
        """Test uploading a file."""
        api_client.force_authenticate(user=user)
        
        data = {
            'file': test_file,
            'idea_id': str(idea.id)
        }
        
        response = api_client.post('/api/v1/documents/upload/', data, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['file_name'] == 'test_document.pdf'
        assert response.data['virus_scan_status'] == 'PENDING'
    
    def test_upload_file_no_file(self, api_client, user, idea):
        """Test uploading without file."""
        api_client.force_authenticate(user=user)
        
        data = {
            'idea_id': str(idea.id)
        }
        
        response = api_client.post('/api/v1/documents/upload/', data, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_upload_file_invalid_idea(self, api_client, user, test_file):
        """Test uploading to invalid idea."""
        api_client.force_authenticate(user=user)
        
        data = {
            'file': test_file,
            'idea_id': '00000000-0000-0000-0000-000000000000'
        }
        
        response = api_client.post('/api/v1/documents/upload/', data, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_list_documents(self, api_client, user, idea, test_file):
        """Test listing documents."""
        api_client.force_authenticate(user=user)
        
        # Create document
        Document.objects.create(
            idea=idea,
            file_name='test.pdf',
            file_path='ideas/test.pdf',
            file_size=1024,
            file_type='pdf',
            uploaded_by=user,
            virus_scan_status='CLEAN'
        )
        
        response = api_client.get('/api/v1/documents/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_get_document_detail(self, api_client, user, idea):
        """Test getting document details."""
        api_client.force_authenticate(user=user)
        
        document = Document.objects.create(
            idea=idea,
            file_name='test.pdf',
            file_path='ideas/test.pdf',
            file_size=1024,
            file_type='pdf',
            uploaded_by=user,
            virus_scan_status='CLEAN'
        )
        
        response = api_client.get(f'/api/v1/documents/{document.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['file_name'] == 'test.pdf'
    
    def test_delete_document(self, api_client, user, idea):
        """Test deleting a document."""
        api_client.force_authenticate(user=user)
        
        document = Document.objects.create(
            idea=idea,
            file_name='test.pdf',
            file_path='ideas/test.pdf',
            file_size=1024,
            file_type='pdf',
            uploaded_by=user,
            virus_scan_status='CLEAN'
        )
        
        response = api_client.delete(f'/api/v1/documents/{document.id}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_filter_by_virus_scan_status(self, api_client, user, idea):
        """Test filtering documents by virus scan status."""
        api_client.force_authenticate(user=user)
        
        Document.objects.create(
            idea=idea,
            file_name='clean.pdf',
            file_path='ideas/clean.pdf',
            file_size=1024,
            file_type='pdf',
            uploaded_by=user,
            virus_scan_status='CLEAN'
        )
        
        Document.objects.create(
            idea=idea,
            file_name='pending.pdf',
            file_path='ideas/pending.pdf',
            file_size=1024,
            file_type='pdf',
            uploaded_by=user,
            virus_scan_status='PENDING'
        )
        
        response = api_client.get('/api/v1/documents/?virus_scan_status=CLEAN')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_scan_status(self, api_client, user, idea):
        """Test getting scan status."""
        api_client.force_authenticate(user=user)
        
        document = Document.objects.create(
            idea=idea,
            file_name='test.pdf',
            file_path='ideas/test.pdf',
            file_size=1024,
            file_type='pdf',
            uploaded_by=user,
            virus_scan_status='CLEAN',
            virus_scan_result='No virus detected'
        )
        
        response = api_client.get(f'/api/v1/documents/{document.id}/scan_status/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'CLEAN'
    
    def test_unauthorized_upload(self, api_client, test_file):
        """Test unauthorized file upload."""
        data = {
            'file': test_file,
            'idea_id': '00000000-0000-0000-0000-000000000000'
        }
        
        response = api_client.post('/api/v1/documents/upload/', data, format='multipart')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
