"""
Custom middleware for the application.
"""

import logging
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(MiddlewareMixin):
    """Middleware for handling errors and logging."""
    
    def process_exception(self, request, exception):
        """Handle exceptions and return JSON response."""
        logger.error(f"Exception: {str(exception)}", exc_info=True)
        
        return JsonResponse({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An internal server error occurred.',
                'detail': str(exception) if settings.DEBUG else None
            }
        }, status=500)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware for logging requests and responses."""
    
    def process_request(self, request):
        """Log incoming request."""
        logger.info(f"Request: {request.method} {request.path}")
        return None
    
    def process_response(self, request, response):
        """Log outgoing response."""
        logger.info(f"Response: {request.method} {request.path} {response.status_code}")
        return response


class CORSMiddleware(MiddlewareMixin):
    """Middleware for handling CORS headers."""
    
    def process_response(self, request, response):
        """Add CORS headers to response."""
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
