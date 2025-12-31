"""
Tests for Ideas app.
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Idea, Campaign, Contributor, Document
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
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def admin_user(db):
    """Create test admin user."""
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        is_staff=True
    )


@pytest.fixture
def campaign(db):
    """Create test campaign."""
    return Campaign.objects.create(
        name='Q1 2024 Innovation Challenge',
        description='Submit your innovative ideas for Q1 2024',
        status='ACTIVE',
        start_date=datetime.now().date(),
        end_date=(datetime.now() + timedelta(days=30)).date()
    )


@pytest.fixture
def idea(db, user, campaign):
    """Create test idea."""
    idea = Idea.objects.create(
        title='Test Idea',
        description='This is a test idea',
        expected_impact='HIGH',
        submitter=user,
        campaign=campaign,
        status='DRAFT'
    )
    # Add submitter as contributor
    Contributor.objects.create(
        idea=idea,
        user=user,
        role='SUBMITTER'
    )
    return idea


class TestIdeaViewSet:
    """Tests for IdeaViewSet."""
    
    def test_create_idea(self, api_client, user, campaign):
        """Test creating an idea."""
        api_client.force_authenticate(user=user)
        
        data = {
            'title': 'New Idea',
            'description': 'This is a new idea',
            'expected_impact': 'MEDIUM',
            'campaign_id': str(campaign.id)
        }
        
        response = api_client.post('/api/v1/ideas/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Idea'
        assert response.data['status'] == 'DRAFT'
    
    def test_list_ideas(self, api_client, user, idea):
        """Test listing ideas."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/ideas/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_get_idea_detail(self, api_client, user, idea):
        """Test getting idea details."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get(f'/api/v1/ideas/{idea.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == idea.title
    
    def test_update_idea(self, api_client, user, idea):
        """Test updating an idea."""
        api_client.force_authenticate(user=user)
        
        data = {
            'title': 'Updated Idea',
            'description': 'Updated description',
            'expected_impact': 'LOW'
        }
        
        response = api_client.put(f'/api/v1/ideas/{idea.id}/', data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Idea'
    
    def test_delete_idea(self, api_client, user, idea):
        """Test deleting an idea."""
        api_client.force_authenticate(user=user)
        
        response = api_client.delete(f'/api/v1/ideas/{idea.id}/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_submit_idea(self, api_client, user, idea):
        """Test submitting a draft idea."""
        api_client.force_authenticate(user=user)
        
        response = api_client.post(f'/api/v1/ideas/{idea.id}/submit/', {})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'SUBMITTED'
    
    def test_add_contributor(self, api_client, user, idea, db):
        """Test adding a contributor."""
        api_client.force_authenticate(user=user)
        
        contributor_user = User.objects.create_user(
            username='contributor',
            email='contributor@example.com',
            password='pass123'
        )
        
        data = {'user_id': contributor_user.id}
        
        response = api_client.post(f'/api/v1/ideas/{idea.id}/add_contributor/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_list_contributors(self, api_client, user, idea):
        """Test listing contributors."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get(f'/api/v1/ideas/{idea.id}/contributors/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
    
    def test_my_ideas(self, api_client, user, idea):
        """Test getting user's ideas."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/ideas/my/')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_filter_by_status(self, api_client, user, idea):
        """Test filtering ideas by status."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/ideas/?status=DRAFT')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_search_ideas(self, api_client, user, idea):
        """Test searching ideas."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/ideas/?search=Test')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_unauthorized_access(self, api_client):
        """Test unauthorized access."""
        response = api_client.get('/api/v1/ideas/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_permission_denied_update(self, api_client, user, idea, db):
        """Test permission denied for updating other's idea."""
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass123'
        )
        
        api_client.force_authenticate(user=other_user)
        
        data = {'title': 'Hacked Title'}
        
        response = api_client.put(f'/api/v1/ideas/{idea.id}/', data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestCampaignViewSet:
    """Tests for CampaignViewSet."""
    
    def test_list_campaigns(self, api_client, user, campaign):
        """Test listing campaigns."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/campaigns/')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_campaign_detail(self, api_client, user, campaign):
        """Test getting campaign details."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get(f'/api/v1/campaigns/{campaign.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == campaign.name


class TestContributorViewSet:
    """Tests for ContributorViewSet."""
    
    def test_list_contributors(self, api_client, user, idea):
        """Test listing contributors."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/contributors/')
        
        assert response.status_code == status.HTTP_200_OK


class TestDocumentViewSet:
    """Tests for DocumentViewSet."""
    
    def test_list_documents(self, api_client, user, idea):
        """Test listing documents."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/documents/')
        
        assert response.status_code == status.HTTP_200_OK
