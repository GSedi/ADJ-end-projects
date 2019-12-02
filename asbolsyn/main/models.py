from django.db import models
from django.db.models import Avg, Max, Min, Sum, Count

from users.models import MainUser as User
from locations.models import Address
from utils import upload, validators, constants


class PlaceManager(models.Manager):
    def get_by_country(self, country):
        return self.filter(address__town__country=country)

    def get_by_town(self, town):
        return self.filter(address__town=town)


class BusinessCenterManager(PlaceManager):
    def filter_by_name(self, name):
        return self.filter(name__contains=name)


class BusinessCenter(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, default=None)
    image = models.FileField(upload_to=upload.business_center_image_path,
                             validators=[validators.image_size, validators.image_extension],
                             default=None,
                             null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_business_centers')

    objects = BusinessCenterManager()

    def __str__(self):
        return self.name


class RestaurantManager(PlaceManager):
    def filter_by_name(self, name):
        return self.filter(name__contains=name)


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, default=None)
    image = models.FileField(upload_to=upload.restaurant_image_path,
                             validators=[validators.image_size, validators.image_extension],
                             default=None,
                             null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_restaurants')

    objects = RestaurantManager()

    def __str__(self):
        return self.name


class BaseMenu(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, default=None)
    image = models.FileField()
    is_hidden = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(null=True, default=None)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class MenuManagerBase(models.Manager):
    def not_hidden(self):
        return self.filter(is_hidden=False)

    def filter_by_name(self, name):
        return self.filter(name__contains=name)

    def filter_by_creator(self, creator):
        return self.filter(created_by=creator)

    def order_by(self, field="priority", asc=""):
        return self.order_by(asc+field)


class MenuManager(MenuManagerBase):
    def by_restaurant(self, restaurant):
        return self.filter(restaurant=restaurant)


class Menu(BaseMenu):
    image = models.FileField(upload_to=upload.menu_image_path,
                             validators=[validators.image_size, validators.image_extension],
                             default=None,
                             null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='menus')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')

    objects = MenuManager()

    def __str__(self):
        return self.name


class MenuItemManager(MenuManagerBase):
    def by_menu(self, menu):
        return self.filter(menu=menu)


class MenuItem(BaseMenu):
    image = models.FileField(upload_to=upload.menu_item_image_path,
                             validators=[validators.image_size, validators.image_extension],
                             default=None,
                             null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_menu_items')
    price = models.PositiveIntegerField()
    with_garnish = models.BooleanField(default=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_items')

    objects = MenuItemManager()


class OrderManager(models.Manager):
    def by_user(self, user):
        return self.filter(user=user)

    def order_by(self, field="amount", asc=""):
        return self.order_by(asc+field)

    def by_status(self, status):
        return self.filter(status=status)

    def get_max_amount(self):
        return self.filter(status=constants.ORDER_PAYED).aggregate(Max('amount'))

    def get_min_amount(self):
        return self.filter(status=constants.ORDER_PAYED).aggregate(Min('amount'))

    def get_avg_amount(self):
        return self.filter(status=constants.ORDER_PAYED).aggregate(Avg('amount'))

    def get_sum_amount(self):
        return self.filter(status=constants.ORDER_PAYED).aggregate(Sum('amount'))

    def get_cnt_menu_items_for_order(self, order):
        return self.filter(order=order).aggregate(menu_items_count=Count('order_menu_items'))

    def get_cnt_menu_items(self):
        return self.annotate(menu_items_count=Count('order_menu_items'))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='orders')
    amount = models.PositiveIntegerField()
    comment = models.TextField()
    status = models.PositiveSmallIntegerField(choices=constants.ORDER_STATUSES, default=constants.ORDER_CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()


class OrderMenuItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_menu_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order\'s menu item'
        verbose_name_plural = 'Order\'s menu items'
