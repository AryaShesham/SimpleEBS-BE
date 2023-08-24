from rest_framework import permissions


class IsEventOrganiser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'eventorganiser')


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'customer')
