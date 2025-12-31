"""
Permissions for Ideas app.
"""

from rest_framework import permissions


class IsSubmitterOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only submitters to edit their ideas.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the submitter
        return obj.submitter == request.user


class IsContributor(permissions.BasePermission):
    """
    Permission to check if user is a contributor to the idea.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()


class IsPanelMember(permissions.BasePermission):
    """
    Permission to check if user is a panel member.
    """
    
    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.role == 'PANEL_MEMBER'


class IsAdmin(permissions.BasePermission):
    """
    Permission to check if user is an admin.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
