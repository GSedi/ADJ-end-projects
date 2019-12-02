from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from main.models import BusinessCenter, Menu, MenuItem, Restaurant, Order, OrderMenuItem
from utils import upload

_UNSAVED_FILEFIELD = 'unsaved_filefield'


@receiver(pre_save, sender=BusinessCenter)
@receiver(pre_save, sender=Restaurant)
@receiver(pre_save, sender=Menu)
@receiver(pre_save, sender=MenuItem)
def skip_saving_file(sender, instance, **kwargs):
    if not instance.id and not hasattr(instance, _UNSAVED_FILEFIELD):
        setattr(instance, _UNSAVED_FILEFIELD, instance.image)
        instance.image = None


@receiver(post_save, sender=BusinessCenter)
@receiver(post_save, sender=Restaurant)
@receiver(post_save, sender=Menu)
@receiver(post_save, sender=MenuItem)
def save_file(sender, instance, created, **kwargs):
    if created and hasattr(instance, _UNSAVED_FILEFIELD):
        instance.image = getattr(instance, _UNSAVED_FILEFIELD)
        instance.save()
        instance.__dict__.pop(_UNSAVED_FILEFIELD)


@receiver(post_delete, sender=BusinessCenter)
def business_center_deleted(sender, instance, **kwargs):
    upload.business_center_delete_path(instance)


@receiver(post_delete, sender=Restaurant)
def business_center_deleted(sender, instance, **kwargs):
    upload.restaurant_delete_path(instance)


@receiver(post_delete, sender=Menu)
def menu_deleted(sender, instance, **kwargs):
    upload.menu_delete_path(instance)


@receiver(post_delete, sender=MenuItem)
def menu_item_deleted(sender, instance, **kwargs):
    upload.menu_item_delete_path(instance)


# @receiver(post_save, sender=Order)
# def order_pre_save(sender, instance, **kwargs):
#     pass