from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.http import HttpRequest


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST" and request.user and request.user.is_authenticated:
            return True
        return bool(request.method in SAFE_METHODS)


class IsOwnerOrAdminUserOrReadOnly(BasePermission):

    def has_object_permission(self, request: HttpRequest, view, obj):
        if request.method in SAFE_METHODS or obj.user == request.user:
            return True

        if (
                request.method in ["PUT", "PATCH"]
                and (request.user.has_perm("beer_BLR.change_experience")
                     and obj.user == request.user
                     or request.user.is_staff)
        ):
            return True

        if (
                request.method in ["DELETE"]
                and (request.user.has_perm("beer_BLR.delete_experience")
                     and obj.user == request.user
                     or request.user.is_staff)

        ):
            return True

        return False

