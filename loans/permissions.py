from rest_framework import permissions


class IsLoanOwnerOrAdmin(permissions.BasePermission):
    """
    Owners: can only read their own loans.
    Admins: can read and modify all loans.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for owner or admin
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user or request.user.is_staff

        # Write permissions only for admins
        return request.user and request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admins can modify, users can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsRepaymentOwnerOrAdmin(permissions.BasePermission):
    """
    Owners: can only read their own repayments.
    Admins: can read and modify all repayments.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for repayment owner or admin
        if request.method in permissions.SAFE_METHODS:
            return obj.loan.user == request.user or request.user.is_staff

        # Write permissions only for admins
        return request.user and request.user.is_staff
