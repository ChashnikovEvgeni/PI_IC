from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.owner == request.user or request.user.is_staff)
        )


class IsAccess(permissions.BasePermission):
  def has_permission(self, request, view):
        if request.user.profile.position == 'Administrator' or request.user.profile.position=='Department/Group Leadership' or request.user.profile.position=='Service manager':
            return  True
        return False

class IsEditor(permissions.BasePermission):
  def has_permission(self, request, view):
        if request.user.profile.position == 'Administrator' or request.user.profile.position=='Service manager':
            return  True
        return False