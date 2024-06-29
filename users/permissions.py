from rest_framework.permissions import BasePermission


class IsRealUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False
