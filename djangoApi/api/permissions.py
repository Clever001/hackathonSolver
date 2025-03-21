from rest_framework import permissions
from .models import Request


class IsSuperuserOrPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_superuser
                or request.method == "POST"
        )


class IsSuperuserOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user


class RequestDetailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.author.id == request.user.id


class SafeOrSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                (request.method in permissions.SAFE_METHODS and request.user.is_authenticated)
                or request.user.is_superuser
        )
