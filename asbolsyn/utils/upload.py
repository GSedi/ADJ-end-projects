import os
import shutil
from django.conf import settings


def profile_image_path(instance, filename):
    user_id = instance.user.id
    return f'images/profiles/{user_id}/{filename}'


def profile_delete_path(instance):
    dirpath = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        f'images/profiles/{instance.user.id}'))
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

def business_center_image_path(instance, filename):
    return f'images/business_centers/{instance.id}/{filename}'


def business_center_delete_path(instance):
    dirpath = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        f'images/business_centers/{instance.id}'))
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)


def restaurant_image_path(instance, filename):
    return f'images/restaurants/{instance.id}/{filename}'


def restaurant_delete_path(instance):
    dirpath = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        f'images/restaurants/{instance.id}'))
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

def menu_image_path(instance, filename):
    return f'images/menus/{instance.id}/{filename}'


def menu_delete_path(instance):
    dirpath = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        f'images/menus/{instance.id}'))
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)


def menu_item_image_path(instance, filename):
    return f'images/menu_items/{instance.id}/{filename}'


def menu_item_delete_path(instance):
    dirpath = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        f'images/menu_items/{instance.id}'))
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
