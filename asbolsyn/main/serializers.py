from rest_framework import serializers
from django.db import transaction

from main.models import BusinessCenter, Menu, MenuItem, Order, OrderMenuItem, Restaurant
from users.serializers import MainUserSerializer
from locations.serializers import AddressSerializer
from locations.models import Address
from utils import constants


class BusinessCenterShortSerializer(serializers.ModelSerializer):
    address_id = serializers.IntegerField(write_only=True, required=False)
    address_title = serializers.SerializerMethodField(read_only=True)
    image = serializers.FileField(required=False)

    class Meta:
        model = BusinessCenter
        fields = ('id', 'name', 'image', 'address_id', 'address_title')

    def get_address_title(self, obj):
        if obj.address is not None:
            return obj.address.address
        return ''

    def validate_name(self, value):
        if len(value) <= 3:
            raise serializers.ValidationError('Name length must be more than 3 char-s')
        return value


class BusinessCenterFullSerializer(BusinessCenterShortSerializer):
    address = AddressSerializer(required=False)

    def __init__(self, *args, **kwargs):
        super(BusinessCenterFullSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('address_title')

    class Meta(BusinessCenterShortSerializer.Meta):
        fields = BusinessCenterShortSerializer.Meta.fields + ('description', 'address')

    def create(self, validated_data):
        with transaction.atomic():
            if validated_data.__contains__('address'):
                address_data = validated_data.pop('address')
                address = Address.objects.create(**address_data)
                business_center = BusinessCenter.objects.create(address=address, **validated_data)
            elif validated_data.__contains__('address_id'):
                business_center = BusinessCenter.objects.create(**validated_data)
            else:
                raise serializers.ValidationError('address or address_id were not provided')
        return business_center


class RestaurantShortSerializer(serializers.ModelSerializer):
    address_id = serializers.IntegerField(write_only=True, required=False)
    address_title = serializers.SerializerMethodField(read_only=True)
    image = serializers.FileField(required=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'image', 'address_id', 'address_title')

    def get_address_title(self, obj):
        if obj.address is not None:
            return obj.address.address
        return ''

    def validate_name(self, value):
        if len(value) <= 3:
            raise serializers.ValidationError('Name length must be more than 3 char-s')
        return value

class RestaurantFullSerializer(RestaurantShortSerializer):
    address = AddressSerializer(required=False)

    def __init__(self, *args, **kwargs):
        super(RestaurantFullSerializer, self).__init__(*args, **kwargs)
        self.fields.pop('address_title')

    class Meta(RestaurantShortSerializer.Meta):
        fields = RestaurantShortSerializer.Meta.fields + ('description', 'address')

    def create(self, validated_data):
        with transaction.atomic():
            if validated_data.__contains__('address'):
                address_data = validated_data.pop('address')
                address = Address.objects.create(**address_data)
                restaurant = Restaurant.objects.create(address=address, **validated_data)
            elif validated_data.__contains__('address_id'):
                restaurant = Restaurant.objects.create(**validated_data)
            else:
                raise serializers.ValidationError('address or address_id were not provided')
        return restaurant


class MenuShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'image', 'priority', 'restaurant')

    def validate_name(self, value):
        if len(value) <= 3:
            raise serializers.ValidationError('Name length must be more than 3 char-s')
        return value


class MenuFullSerializer(MenuShortSerializer):
    created_by = MainUserSerializer(read_only=True)
    is_hidden = serializers.BooleanField(write_only=True)

    class Meta(MenuShortSerializer.Meta):
        fields = MenuShortSerializer.Meta.fields + ('description', 'is_hidden', 'created_by')


class MenuItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'image', 'priority', 'price', 'menu')

    def validate_name(self, value):
        if len(value) <= 3:
            raise serializers.ValidationError('Name length must be more than 3 char-s')
        return value


class MenuItemFullSerializer(MenuItemShortSerializer):
    created_by = MainUserSerializer(read_only=True)
    is_hidden = serializers.BooleanField(write_only=True)

    class Meta(MenuItemShortSerializer.Meta):
        fields = MenuItemShortSerializer.Meta.fields + ('description', 'is_hidden', 'created_by', 'with_garnish')


class OrderMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenuItem
        fields = ('id', 'menu_item', 'count')

    def validate_count(self, value):
        if value <= 0:
            raise serializers.ValidationError('Count of menu items must be more than 0')
        return value


class OrderShortSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(read_only=True)
    comment = serializers.CharField(required=False)
    status = serializers.IntegerField(write_only=True)
    status_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'amount', 'comment', 'status', 'status_title')

    def validate_status(self, value):
        d = dict(constants.ORDER_STATUSES)
        if value not in d.keys():
            raise serializers.ValidationError('Order status options: ' + str(d))
        return value

    def get_status_title(self, obj):
        d = dict(constants.ORDER_STATUSES)
        return d[obj.status]


class OrderFullSerializer(OrderShortSerializer):
    order_menu_items = OrderMenuItemSerializer(many=True)

    class Meta(OrderShortSerializer.Meta):
        fields = OrderShortSerializer.Meta.fields + ('order_menu_items',)


    def create(self, validated_data):
        with transaction.atomic():
            if not validated_data.__contains__('order_menu_items'):
                raise serializers.ValidationError('order menu items were not provided')

            order_menu_items = validated_data.pop('order_menu_items')
            validated_data['amount'] = self.calculate_order_amount(order_menu_items)
            order = Order.objects.create(**validated_data)
            self.bulk_order_menu_items_create_or_update(order, order_menu_items)

        return order

    def update(self, instance, validated_data):
        with transaction.atomic():
            if not validated_data.__contains__('order_menu_items'):
                raise serializers.ValidationError('order menu items were not provided')

            order_menu_items = validated_data.pop('order_menu_items')
            validated_data['amount'] = self.calculate_order_amount(order_menu_items)
            Order.objects.filter(id=instance.id).update(**validated_data)
            order = Order.objects.get(id=instance.id)
            self.bulk_order_menu_items_create_or_update(order, order_menu_items)

        return order


    def calculate_order_amount(self, order_menu_items):
        amount = 0
        for order_menu_item in order_menu_items:
            amount += order_menu_item['menu_item'].price * order_menu_item['count']

        return amount

    def bulk_order_menu_items_create_or_update(self, order, order_menu_items):
        for order_menu_item_data in order_menu_items:
            OrderMenuItem.objects.update_or_create(order=order, **order_menu_item_data)
