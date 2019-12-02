from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status as status_codes
from django.core import exceptions
from rest_condition import Or

from main.models import BusinessCenter, Restaurant, Menu, MenuItem, Order, OrderMenuItem
from main.serializers import BusinessCenterShortSerializer, BusinessCenterFullSerializer, RestaurantShortSerializer, \
    RestaurantFullSerializer, MenuShortSerializer, MenuFullSerializer, MenuItemShortSerializer, MenuItemFullSerializer,\
    OrderShortSerializer, OrderFullSerializer, OrderMenuItemSerializer

from utils.permissions import IsOwnerUser, IsStaff, IsClient, IsRestaurantAdministrator, IsCourier,\
    IsOwnerRestaurantAdministrator
from utils import constants
from main.constants import ROLES_ORDER_STATUSES


class BusinessCenterViewSet(viewsets.ModelViewSet):
    queryset = BusinessCenter.objects.all()
    serializer_class = BusinessCenterShortSerializer
    permission_classes = (IsAdminUser, )

    def get_serializer_class(self):
        if self.action in ['list', 'by_town']:
            return BusinessCenterShortSerializer
        else:
            return BusinessCenterFullSerializer

    def get_permissions(self):
        if self.action in ['list', 'by_town', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [Or(IsAdminUser, IsStaff)]
        if self.action in ['update']:
            return [Or(IsAdminUser, IsStaff)]
        return [IsAdminUser]

    @action(methods=['GET'], detail=False)
    def by_town(self, request):
        business_centers = BusinessCenter.objects.get_by_town(request.GET['town'])
        serializer = self.get_serializer(business_centers, many=True)
        return Response(serializer.data)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantShortSerializer

    def get_permissions(self):
        if self.action in ['list', 'by_town', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [Or(IsAdminUser, IsStaff)]
        if self.action in ['update']:
            return [Or(IsAdminUser, IsStaff, IsOwnerRestaurantAdministrator)]
        return [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['list', 'by_town']:
            return RestaurantShortSerializer
        else:
            return RestaurantFullSerializer

    @action(methods=['GET'], detail=False)
    def by_town(self, request):
        restaurants = Restaurant.objects.get_by_town(request.GET['town'])
        serializer = self.get_serializer(restaurants, many=True)
        return Response(serializer.data)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuShortSerializer

    def get_queryset(self):
        return Menu.objects.not_hidden()

    def get_serializer_class(self):
        if self.action in ['list', 'by_restaurant']:
            return MenuShortSerializer
        else:
            return MenuFullSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        if serializer.is_valid():
            serializer.save(created_by=creator)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        restaurant = self.get_object().restaurant
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def by_restaurant(self, request):
        if 'restaurant' not in request.GET.keys():
            raise exceptions.ValidationError('restaurant were not provided')
        menus = Menu.objects.by_restaurant(restaurant=request.GET['restaurant'])
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemShortSerializer

    def get_queryset(self):
        if self.action in ['update']:
            return MenuItem.objects.all()

        return MenuItem.objects.not_hidden()

    def get_serializer_class(self):
        if self.action in ['list', 'by_menu']:
            return MenuItemShortSerializer
        else:
            return MenuItemFullSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        if serializer.is_valid():
            serializer.save(created_by=creator)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        menu = self.get_object().menu
        if serializer.is_valid():
            serializer.save(menu=menu)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def by_menu(self, request):
        if 'menu' not in request.GET.keys():
            raise exceptions.ValidationError('menu were not provided')
        menu_items = MenuItem.objects.by_menu(menu=request.GET['menu'])
        serializer = self.get_serializer(menu_items, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderShortSerializer
    permission_classes = (IsAdminUser, )

    def get_permissions(self):
        if self.action == 'list':
            return [Or(IsRestaurantAdministrator, IsCourier, IsAdminUser)]
        if self.action == 'create':
            return [Or(IsAdminUser, IsClient)]
        if self.action in ['retrieve', 'update', 'by_user']:
            return [Or(IsAdminUser, IsRestaurantAdministrator, IsCourier, IsOwnerUser)]
            # return [Or(IsOwnerUser(), IsAdminUser(), IsCourier(), IsRestaurantAdministrator())]
        return [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['list']:
            return OrderShortSerializer
        else:
            return OrderFullSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        serializer.validated_data['status'] = constants.ORDER_CREATED
        if serializer.is_valid():
            serializer.save(user=creator)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        status = constants.ORDER_CREATED
        if 'status' in serializer.validated_data.keys():
            status = serializer.validated_data['status']

        if self.request.user.role != constants.CLIENT:
            serializer.data.clear()

        serializer.validated_data['status'] = status

        if serializer.validated_data['status'] in ROLES_ORDER_STATUSES[self.request.user.role]:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        raise exceptions.ValidationError('You do not have permission to change status')


    @action(methods=['GET'], detail=False)
    def by_user(self, request):
        orders = Order.objects.by_user(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
