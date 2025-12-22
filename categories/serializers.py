from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Category
from products.serializers import ProductReadSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug', 'description', 'is_active')


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'slug', 'is_active', 'products')

    @extend_schema_field(ProductReadSerializer(many=True))
    def get_products(self, obj):
        return ProductReadSerializer(obj.products.all(), many=True).data