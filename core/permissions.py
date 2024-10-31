from rest_framework.permissions import BasePermission


class IsVerify(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_verify