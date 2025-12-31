"""
Tests for Authentication app.
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


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


class TestUserViewSet:
    """Tests for UserViewSet."""
    
    def test_register_user(self, api_client):
        """Test user registration."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'NewPass123!',
            'password2': 'NewPass123!'
        }
        
        response = api_client.post('/api/v1/auth/users/register/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'
    
    def test_register_user_password_mismatch(self, api_client):
        """Test registration with mismatched passwords."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'NewPass123!',
            'password2': 'DifferentPass123!'
        }
        
        response = api_client.post('/api/v1/auth/users/register/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_user_weak_password(self, api_client):
        """Test registration with weak password."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': '123',
            'password2': '123'
        }
        
        response = api_client.post('/api/v1/auth/users/register/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_current_user(self, api_client, user):
        """Test getting current user."""
        api_client.force_authenticate(user=user)
        
        response = api_client.get('/api/v1/auth/users/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
    
    def test_change_password(self, api_client, user):
        """Test changing password."""
        api_client.force_authenticate(user=user)
        
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewPass123!',
            'new_password2': 'NewPass123!'
        }
        
        response = api_client.post('/api/v1/auth/users/change_password/', data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_change_password_wrong_old_password(self, api_client, user):
        """Test changing password with wrong old password."""
        api_client.force_authenticate(user=user)
        
        data = {
            'old_password': 'wrongpass',
            'new_password': 'NewPass123!',
            'new_password2': 'NewPass123!'
        }
        
        response = api_client.post('/api/v1/auth/users/change_password/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_change_password_mismatch(self, api_client, user):
        """Test changing password with mismatched new passwords."""
        api_client.force_authenticate(user=user)
        
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewPass123!',
            'new_password2': 'DifferentPass123!'
        }
        
        response = api_client.post('/api/v1/auth/users/change_password/', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_unauthorized_access(self, api_client):
        """Test unauthorized access."""
        response = api_client.get('/api/v1/auth/users/me/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
