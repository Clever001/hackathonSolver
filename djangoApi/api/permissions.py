from rest_framework import permissions


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