from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

import logging

from .serializers import MainUserSerializer, CustomUserSerializer
from .models import MainUser
from utils.permissions import IsOwnerUser
from .constants import ROLES_PROFILES, ROLES_PROFILE_SERIALIZERS

logger = logging.getLogger(__name__)


class RegisterAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = MainUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {serializer.data.get('phone')} registered")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MainUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = MainUserSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(methods=['GET'], detail=False)
    def me(self, request):
        self.permission_classes = (IsOwnerUser,)
        logger.error('YEEEEEEEEEEEEEEEEEEEEE')
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated, IsOwnerUser,)

    def get_queryset(self):
        return ROLES_PROFILES[self.request.user.role].objects.all()

    def get_serializer_class(self):
        return ROLES_PROFILE_SERIALIZERS[self.request.user.role]


class CustomUserViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = MainUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser, )
