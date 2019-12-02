from utils import constants

ROLES_ORDER_STATUSES = {
    constants.SUPERUSER: dict(constants.ORDER_STATUSES).keys(),
    constants.DEVELOPER: [],
    constants.CLIENT: [constants.ORDER_CREATED, constants.ORDER_USER_CANCELED],
    constants.RESTAURANT_ADMINISTRATOR: [constants.ORDER_STAFF_CANCELED, constants.ORDER_ACCEPTED,
                                         constants.ORDER_DELIVERING],
    constants.COURIER: [constants.ORDER_DELIVERED, constants.ORDER_PAYED, constants.ORDER_NOT_PAYED]
}