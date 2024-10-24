from drf_yasg import openapi
from .views import ProductView
from django.urls import path, re_path, include
from rest_framework import permissions

urlpatterns = [
    path('list/', ProductView.as_view(), name='productsview'),
]
