# coding=utf-8
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission untuk DRF.
    Untuk membatasi editing user desc hanya oleh user yg login.
    """
    def has_object_permission(self, request, view, obj):
        """Read permissions are allowed to any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        :param obj:
        :param view:
        :param request:
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
