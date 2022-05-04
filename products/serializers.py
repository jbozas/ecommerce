from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'created_at',
            'updated_at',
            'name',
            'price',
            'stock',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )
