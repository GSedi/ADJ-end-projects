from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from utils import constants, upload, validators


class MainUserManager(BaseUserManager):
    def _create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The given username must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class MainUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=10, unique=True)
    password = models.CharField('password', max_length=128, null=True, blank=False)
    role = models.PositiveSmallIntegerField(choices=constants.USER_ROLES, default=constants.CLIENT)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = MainUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    image = models.FileField(upload_to=upload.profile_image_path,
                             validators=[validators.image_size, validators.image_extension],
                             default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class StaffProfile(Profile):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)


class ClientProfile(Profile):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    business_center = models.ForeignKey('main.BusinessCenter', on_delete=models.DO_NOTHING, related_name='bc_clients',
                                        default=None, null=True)


class RestaurantAdminProfile(Profile):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('main.Restaurant', on_delete=models.DO_NOTHING, related_name='restaurant_admins',
                                   null=True, default=None)


class CourierProfile(Profile):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='couriers')
    car = models.CharField(max_length=200)


