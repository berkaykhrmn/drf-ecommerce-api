from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_api_key.models import APIKey


class HasValidAPIKey(BasePermission):
    header_name = 'X-API-KEY'

    def has_permission(self, request, view):
        key = request.headers.get(self.header_name)

        if not key:
            raise AuthenticationFailed('API Key header is missing')

        try:
            APIKey.objects.get_from_key(key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')

        return True


class IsAuthenticatedWithAPIKey(BasePermission):
    def has_permission(self, request, view):
        HasValidAPIKey().has_permission(request, view)

        if not request.user or not request.user.is_authenticated:
            raise AuthenticationFailed('Authentication credentials were not provided')

        return True


class IsAdminWithAPIKey(BasePermission):
    def has_permission(self, request, view):
        HasValidAPIKey().has_permission(request, view)

        if not request.user or not request.user.is_staff:
            raise PermissionDenied('Only staff users can perform this action')

        return True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user