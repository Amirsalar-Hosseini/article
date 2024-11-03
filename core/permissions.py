from rest_framework.permissions import BasePermission


class IsVerify(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verify

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user