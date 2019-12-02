# from users.models import StaffProfile, ClientProfile, RestaurantAdminProfile, CourierProfile

IMAGE_ALLOWED_EXTS = ['.jpg', '.png']

SUPERUSER = 1
DEVELOPER = 2
RESTAURANT_ADMINISTRATOR = 3
COURIER = 4
CLIENT = 5

USER_ROLES = (
    (SUPERUSER, 'superuser'),
    (DEVELOPER, 'developer'),
    (RESTAURANT_ADMINISTRATOR, 'restaurant administrator'),
    (COURIER, 'courier'),
    (CLIENT, 'client')
)

# ROLES_PROFILES = {
#     SUPERUSER: StaffProfile(),
#     DEVELOPER: StaffProfile(),
#     CLIENT: ClientProfile(),
#     RESTAURANT_ADMINISTRATOR: RestaurantAdminProfile(),
#     COURIER: CourierProfile()
# }

ORDER_CREATED = 1
ORDER_ACCEPTED = 2
ORDER_DELIVERING = 3
ORDER_DELIVERED = 4
ORDER_PAYED = 5
ORDER_NOT_PAYED = 6
ORDER_USER_CANCELED = 7
ORDER_STAFF_CANCELED = 8

ORDER_STATUSES = (
    (ORDER_CREATED, 'order created'),
    (ORDER_ACCEPTED, 'order_accepted'),
    (ORDER_DELIVERING, 'order delivering'),
    (ORDER_DELIVERED, 'order delivered'),
    (ORDER_PAYED, 'order payed'),
    (ORDER_USER_CANCELED, 'order canceled by user'),
    (ORDER_STAFF_CANCELED, 'order canceled by staff'),
    (ORDER_NOT_PAYED, 'order not payed')
)
