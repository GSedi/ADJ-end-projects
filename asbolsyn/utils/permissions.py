from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from . import constants


class IsOwnerUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in [constants.SUPERUSER, constants.DEVELOPER]

    def has_object_permission(self, request, view, obj):
        return True


class IsClient(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in [constants.CLIENT]

    def has_object_permission(self, request, view, obj):
        return True


class IsRestaurantAdministrator(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (request.user.role in [constants.RESTAURANT_ADMINISTRATOR])

    def has_object_permission(self, request, view, obj):
        return True


class IsCourier(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in [constants.COURIER]

    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerRestaurantAdministrator(IsRestaurantAdministrator):
    def has_object_permission(self, request, view, obj):
        return request.user in [profile.user for profile in obj.restaurant_admins]
