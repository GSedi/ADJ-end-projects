from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from users.models import MainUser, StaffProfile, ClientProfile, RestaurantAdminProfile, CourierProfile
from utils import upload
from . import constants


@receiver(post_save, sender=MainUser)
def user_registered(sender, instance, created, **kwargs):
    if created:
        constants.ROLES_PROFILES[instance.role].objects.create(user=instance)


@receiver(post_delete, sender=StaffProfile)
@receiver(post_delete, sender=ClientProfile)
@receiver(post_delete, sender=RestaurantAdminProfile)
@receiver(post_delete, sender=CourierProfile)
def profile_deleted(sender, instance, **kwargs):
    upload.profile_delete_path(instance)
