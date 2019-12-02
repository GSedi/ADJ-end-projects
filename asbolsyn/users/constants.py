from users.models import StaffProfile, ClientProfile, RestaurantAdminProfile, CourierProfile
from users.serializers import StaffProfileSerializer, ClientProfileSerializer, RestaurantAdminProfileSerializer, \
    CourierProfileSerializer
from utils import constants

ROLES_PROFILES = {
    constants.SUPERUSER: StaffProfile,
    constants.DEVELOPER: StaffProfile,
    constants.CLIENT: ClientProfile,
    constants.RESTAURANT_ADMINISTRATOR: RestaurantAdminProfile,
    constants.COURIER: CourierProfile
}

ROLES_PROFILE_SERIALIZERS = {
    constants.SUPERUSER: StaffProfileSerializer,
    constants.DEVELOPER: StaffProfileSerializer,
    constants.CLIENT: ClientProfileSerializer,
    constants.RESTAURANT_ADMINISTRATOR: RestaurantAdminProfileSerializer,
    constants.COURIER: CourierProfileSerializer
}
