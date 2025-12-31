"""
Utility functions for the application.
"""

import os
import uuid
from datetime import datetime
from django.core.files.storage import default_storage
from django.conf import settings


def generate_file_path(instance, filename):
    """Generate file path for uploaded files."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('ideas', str(instance.idea.id), filename)


def upload_file_to_s3(file, file_name):
    """Upload file to S3."""
    try:
        path = default_storage.save(f'ideas/{file_name}', file)
        return path
    except Exception as e:
        raise Exception(f"Failed to upload file to S3: {str(e)}")


def delete_file_from_s3(file_path):
    """Delete file from S3."""
    try:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
    except Exception as e:
        raise Exception(f"Failed to delete file from S3: {str(e)}")


def get_file_url(file_path):
    """Get URL for file in S3."""
    try:
        return default_storage.url(file_path)
    except Exception as e:
        raise Exception(f"Failed to get file URL: {str(e)}")


def format_datetime(dt):
    """Format datetime to ISO format."""
    if dt:
        return dt.isoformat()
    return None


def parse_datetime(dt_string):
    """Parse datetime from ISO format."""
    if dt_string:
        return datetime.fromisoformat(dt_string)
    return None


def sanitize_filename(filename):
    """Sanitize filename to prevent directory traversal."""
    # Remove path separators
    filename = filename.replace('/', '').replace('\\', '')
    # Remove special characters
    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
    return filename


def validate_file_size(file, max_size_mb=10):
    """Validate file size."""
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        raise ValueError(f"File size exceeds {max_size_mb}MB limit")
    return True


def validate_file_type(file, allowed_types=None):
    """Validate file type."""
    if allowed_types is None:
        allowed_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'jpg', 'jpeg', 'png']
    
    ext = file.name.split('.')[-1].lower()
    if ext not in allowed_types:
        raise ValueError(f"File type {ext} is not allowed")
    return True
