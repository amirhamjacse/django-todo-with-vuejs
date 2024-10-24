from .models import Products
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'name',
            'description',
            'product_id',
            'is_active',
            'product_in_date',
        ]
