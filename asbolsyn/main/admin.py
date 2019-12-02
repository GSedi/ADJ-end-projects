from django.contrib import admin

from main.models import BusinessCenter, Menu, MenuItem, \
    Order, OrderMenuItem, Restaurant


admin.site.register(BusinessCenter)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderMenuItem)
