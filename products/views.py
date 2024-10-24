from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import Products
from .serializers import ProductSerializer
from rest_framework.views import APIView


class ProductView(APIView):
    def get(self, request):
        product_object = Products.objects.all()
        serialize = ProductSerializer(product_object, many=True)
        return Response(data = serialize.data, status=status.HTTP_200_OK)
