from rest_framework import serializers
from rest_framework.response import Response

import logging

from users.models import MainUser, Profile, StaffProfile, ClientProfile, RestaurantAdminProfile, CourierProfile
from utils import constants
from . import constants as users_constants

logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'image')


class StaffProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        model = StaffProfile


class ClientProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        model = ClientProfile
        fields = ProfileSerializer.Meta.fields + ('business_center', )


class RestaurantAdminProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        model = RestaurantAdminProfile
        fields = ProfileSerializer.Meta.fields + ('restaurant', )


class CourierProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        model = CourierProfile
        fields = ProfileSerializer.Meta.fields + ('car', )


class MainUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(read_only=True)
    role = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'phone', 'password', 'role', 'profile')

    def create(self, validated_data):
        logger.info("something normal")
        user = MainUser.objects.create_user(**validated_data)
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.SerializerMethodField(read_only=True)
    role = serializers.IntegerField()

    class Meta:
        model = MainUser
        fields = ('id', 'phone', 'password', 'role', 'profile')

    def create(self, validated_data):
        logger.info("something normal")
        user = MainUser.objects.create_user(**validated_data)
        return user

    def validate_role(self, value):
        d = dict(constants.USER_ROLES)
        if value not in d.keys():
            raise serializers.ValidationError('Role options: ' + str(d))
        return value

    def get_profile(self, obj):
        profile = users_constants.ROLES_PROFILES[obj.role].objects.get(user=obj.id)
        serializer = users_constants.ROLES_PROFILE_SERIALIZERS[obj.role](profile)
        return serializer.data
