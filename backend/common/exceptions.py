"""
Custom exceptions for the application.
"""

from rest_framework.exceptions import APIException


class ValidationError(APIException):
    """Custom validation error."""
    status_code = 400
    default_detail = 'Validation error.'
    default_code = 'validation_error'


class NotFoundError(APIException):
    """Custom not found error."""
    status_code = 404
    default_detail = 'Resource not found.'
    default_code = 'not_found'


class PermissionDeniedError(APIException):
    """Custom permission denied error."""
    status_code = 403
    default_detail = 'Permission denied.'
    default_code = 'permission_denied'


class ConflictError(APIException):
    """Custom conflict error."""
    status_code = 409
    default_detail = 'Conflict.'
    default_code = 'conflict'


class VirusDetectedError(APIException):
    """Error when virus is detected in uploaded file."""
    status_code = 400
    default_detail = 'Virus detected in uploaded file.'
    default_code = 'virus_detected'


class FileUploadError(APIException):
    """Error during file upload."""
    status_code = 400
    default_detail = 'File upload failed.'
    default_code = 'file_upload_error'
