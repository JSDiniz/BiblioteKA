from rest_framework import permissions
from rest_framework.views import View

from .models import User


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated and obj == request.user:
            return True

        return bool(request.user and request.is_staff)
