from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from users.views import RegisterAPIView, MainUserViewSet, ProfileViewSet, CustomUserViewSet

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', RegisterAPIView.as_view())
]

router = DefaultRouter()
router.register('users', MainUserViewSet, base_name='users')
router.register('profiles', ProfileViewSet, base_name='users')
router.register('custom_users', CustomUserViewSet, base_name='users')


urlpatterns += router.urls
