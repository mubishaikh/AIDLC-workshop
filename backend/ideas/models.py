"""
Domain models for Idea Submission & Management.
"""

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Campaign(models.Model):
    """Campaign model for organizing ideas."""
    
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return self.name


class Idea(models.Model):
    """Idea model for submitted ideas."""
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_EVALUATION', 'Under Evaluation'),
        ('EVALUATED', 'Evaluated'),
        ('RECOGNIZED', 'Recognized'),
    ]
    
    IMPACT_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    expected_impact = models.CharField(max_length=20, choices=IMPACT_CHOICES)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_ideas')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='ideas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    recognized_at = models.DateTimeField(null=True, blank=True)
    
    # Search vector for full-text search
    search_vector = SearchVectorField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['submitter', 'status']),
            models.Index(fields=['campaign', 'status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            GinIndex(fields=['search_vector']),
        ]
        unique_together = [['title', 'campaign']]
    
    def __str__(self):
        return self.title


class Contributor(models.Model):
    """Contributor model for idea contributors."""
    
    ROLE_CHOICES = [
        ('SUBMITTER', 'Submitter'),
        ('CONTRIBUTOR', 'Contributor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='contributors')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributed_ideas')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['added_at']
        indexes = [
            models.Index(fields=['idea', 'user']),
        ]
        unique_together = [['idea', 'user']]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.idea.title}"


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
    uploaded_at = models.DateTimeField(auto_now_add=True)
    virus_scan_status = models.CharField(
        max_length=20,
        choices=VIRUS_SCAN_STATUS_CHOICES,
        default='PENDING'
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['idea', '-uploaded_at']),
        ]
    
    def __str__(self):
        return self.file_name
