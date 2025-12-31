"""
URL configuration for Ideas app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IdeaViewSet, CampaignViewSet, ContributorViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'ideas', IdeaViewSet, basename='idea')
router.register(r'contributors', ContributorViewSet, basename='contributor')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
]
