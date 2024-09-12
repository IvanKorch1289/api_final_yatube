from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Класс проверки прав для автора и комментариев"""
    def has_object_permission(self, request, view, obj):
        super().has_object_permission(request, view, obj)
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )
