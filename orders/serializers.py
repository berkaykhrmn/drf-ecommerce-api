from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductReadSerializer
from typing import Dict

class OrderCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    line1 = serializers.CharField(max_length=255)
    line2 = serializers.CharField(max_length=255, allow_blank=True, required=False)
    city = serializers.CharField(max_length=100)
    district = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=50)

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "updated_at", "status", "order_total", "items", "delivery_address"
        ]

    def get_delivery_address(self, obj) -> Dict[str, str]:
        return {
            'full_name': obj.full_name,
            'email': obj.email,
            'phone_number': obj.phone_number,
            'line1': obj.line1,
            'line2': obj.line2,
            'city': obj.city,
            'district': obj.district,
            'postal_code': obj.postal_code,
            'country': obj.country,
        }