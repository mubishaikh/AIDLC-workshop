"""
Models for Documents app.
"""

import uuid
from django.db import models
from ideas.models import Idea


class Document(models.Model):
    """Document model for uploaded files."""
    
    VIRUS_SCAN_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CLEAN', 'Clean'),
        ('INFECTED', 'Infected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='documents')
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.IntegerField()
    file_type = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    virus_scan_status = models.CharField(
        max_length=20,
        choices=VIRUS_SCAN_STATUS_CHOICES,
        default='PENDING'
    )
    virus_scan_result = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['idea', '-uploaded_at']),
            models.Index(fields=['virus_scan_status']),
        ]
    
    def __str__(self):
        return self.file_name
    
    def get_file_url(self):
        """Get URL for file in S3."""
        from common.utils import get_file_url
        return get_file_url(self.file_path)
