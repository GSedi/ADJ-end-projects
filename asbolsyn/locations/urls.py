from django.urls import path

from ._views import country_lists, country_detail, TownListAPIView, TownDetailAPIView, AddressListAPIView, \
    AddressDetailAPIView

urlpatterns = [
    path('countries/', country_lists),
    path('countries/<int:pk>/', country_detail),

    path('towns/', TownListAPIView.as_view()),
    path('towns/<int:pk>/', TownDetailAPIView.as_view()),

    path('addresses/', AddressListAPIView.as_view()),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view()),
]
