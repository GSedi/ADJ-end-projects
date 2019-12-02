from django.contrib import admin
from locations.models import Country, Town, Address

admin.site.register(Country)
admin.site.register(Town)
admin.site.register(Address)
