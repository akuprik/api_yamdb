from rest_framework import permissions


class IsAdministratorOrSuperUser(permissions.BasePermission):
    """
    чтение и изменения администратору и суперпользователю
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin' \
               or request.user.is_superuser
