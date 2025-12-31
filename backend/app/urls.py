"""
URL configuration for Ideation Portal backend.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# API Router
router = routers.DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/', include([
        # Authentication
        path('auth/', include([
            path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('', include('auth_app.urls')),
        ])),
        
        # Ideas
        path('ideas/', include('ideas.urls')),
        
        # Contributors
        path('contributors/', include('contributors.urls')),
        
        # Campaigns
        path('campaigns/', include('campaigns.urls')),
        
        # Documents
        path('documents/', include('documents.urls')),
        
        # Health check
        path('health/', lambda request: __import__('django.http').JsonResponse({'status': 'ok'})),
    ])),
    
    # Router
    path('api/v1/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
