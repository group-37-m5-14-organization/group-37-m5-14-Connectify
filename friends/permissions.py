from rest_framework import permissions


class AccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj, pk=""):
        ...
