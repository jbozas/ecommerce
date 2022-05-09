from django.forms import ValidationError
from rest_framework import serializers

from utils.errors import ProductOrStockNotFound

from products.serializers import ProductSerializer
from orders.models import Order, OrderDetail
from products.models import Product


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderDetail
        fields = (
            'product',
            'quantity',
        )
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):

    details = OrderDetailSerializer(many=True)
    total_ARS = serializers.SerializerMethodField()
    total_USD = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'date_time',
            'details',
            'total_ARS',
            'total_USD'
        )
        read_only_fields = (
            'id',
            'date_time',
            'total_ARS',
            'total_USD'
        )

    def get_total_ARS(self, instance):
        return instance.get_total

    def get_total_USD(self, instance):
        return instance.get_total_in_dollars

    def is_valid(self):
        for data in self.initial_data.get('details'):
            try:
                quantity = data.get('quantity')
                product = Product.objects.get(**data.get('product'))
            except Exception:
                raise ProductOrStockNotFound('Product not found.')
            if not product.has_stock(quantity=quantity):
                raise ValidationError(
                    f'Stock not enough for product {product.id}.')
        return super(OrderSerializer, self).is_valid()

    def create(self, validated_data):
        order = Order.objects.create()
        for detail in self.initial_data.get('details'):
            try:
                quantity = detail.get('quantity')
                product = Product.objects.get(**detail.get('product'))
                OrderDetail.create(
                    order=order, product=product, quantity=quantity)
            except ProductOrStockNotFound:
                raise ValidationError(
                    'Order Detail failed because a missing product.')
        return order
