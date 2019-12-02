from django.urls import path
from rest_framework import routers

from ._views import BusinessCenterViewSet, RestaurantViewSet, MenuViewSet, MenuItemViewSet, OrderViewSet

urlpatterns = []

router = routers.DefaultRouter()

router.register('business_centers', BusinessCenterViewSet, base_name='main')
router.register('restaurants', RestaurantViewSet, base_name='main')
router.register('menus', MenuViewSet, base_name='main')
router.register('menu_items', MenuItemViewSet, base_name='main')
router.register('orders', OrderViewSet, base_name='main')

urlpatterns += router.urls
