from django.contrib import admin

from users.models import MainUser, Profile, StaffProfile, ClientProfile, RestaurantAdminProfile, CourierProfile
from utils import constants


class MyProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


class StaffProfileInline(MyProfile):
    model = StaffProfile

    roles = [constants.SUPERUSER, constants.DEVELOPER]


class ClientProfileInline(MyProfile):
    model = ClientProfile

    roles = [constants.CLIENT]


class RestaurantAdminProfileInline(MyProfile):
    model = RestaurantAdminProfile

    roles = [constants.RESTAURANT_ADMINISTRATOR]


class CourierProfileInline(MyProfile):
    model = CourierProfile

    roles = [constants.COURIER]


@admin.register(MainUser)
class MainUserAdmin(admin.ModelAdmin):
    inlines = [StaffProfileInline, ClientProfileInline, RestaurantAdminProfileInline, CourierProfileInline]
    list_display = ('id', 'phone', 'role', 'is_superuser', 'is_active')

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines if obj.role in inline.roles]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'image')


@admin.register(StaffProfile)
class StaffProfileAdmin(ProfileAdmin):
    list_display = ProfileAdmin.list_display


@admin.register(ClientProfile)
class ClientProfileAdmin(ProfileAdmin):
    list_display = ProfileAdmin.list_display + ('business_center', )


@admin.register(RestaurantAdminProfile)
class RestaurantAdminProfileAdmin(ProfileAdmin):
    list_display = ProfileAdmin.list_display + ('restaurant', )


@admin.register(CourierProfile)
class CourierProfileAdmin(ProfileAdmin):
    list_display = ProfileAdmin.list_display + ('car', )

