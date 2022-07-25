from django.db.models import Q
from django.http import HttpResponse
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
  message = 'Отсутствуют права доступа'
  def has_permission(self, request, view):
      if request.user.groups.filter(Q(name=('Администрация')) | Q(name='Руководство Службы') |  Q(name='Руководство отдела/группы') ).values('name').count() > 0:
          return True
      return False


class AccessIndicator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.department in  request.user.profile.access.all():
            return True
        return False


class IsCreator(permissions.BasePermission):
  message = 'Отсутствуют права доступа'
  def has_permission(self, request, view):
      if request.user.groups.filter(Q(name=('Администрация')) | Q(name='Руководство Службы')).values(
              'name').count() > 0:
          return True
      return False

