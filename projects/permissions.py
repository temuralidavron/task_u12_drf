from rest_framework import permissions

from .models import Project


class IsProjectOwnerOrMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = obj if isinstance(obj, Project) else obj.project
        is_owner = project.owner_id == request.user.id
        if request.method in permissions.SAFE_METHODS:
            return is_owner or project.members.filter(pk=request.user.pk).exists()
        return is_owner



class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff==True
