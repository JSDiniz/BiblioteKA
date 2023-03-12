from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Loan


class IsAdminOrLoanOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Loan):
        return request.user.is_employee or request.user == obj.borrower