from rest_framework import permissions

from .constants import ADMIN


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == ADMIN
