from rest_framework import permissions
from .models import User


class IsAdministratorOrSuperUser(permissions.BasePermission):
    """
    чтение и изменения администратору и суперпользователю
    """
    def has_permission(self, request, view):
        return request.user.is_admin
