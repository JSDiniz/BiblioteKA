from rest_framework import permissions
from rest_framework.views import View, Request

from .models import User


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_employee or request.user == obj.id


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated and
            request.user.is_employee
        )