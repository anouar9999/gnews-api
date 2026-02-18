from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Only allow admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'admin'


class IsAdminOrEditorOrReadOnly(BasePermission):
    """
    - GET: anyone
    - POST/PUT/PATCH: admin or editor
    - DELETE: admin only
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == 'DELETE':
            return request.user.user_type == 'admin'

        return request.user.user_type in ('admin', 'editor')
