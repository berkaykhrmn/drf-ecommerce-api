from rest_framework import serializers
from .models import Product
from . import validations
from categories.models import Category

class ProductWriteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        error_messages={
            'does_not_exist': 'Invalid category',
            'incorrect_type': 'Category id must be numeric'
        }
    )

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'stock': {'required': False},
            'is_active': {'required': False},
        }

    def validate_title(self, value):
        return validations.validate_title(value)

    def validate_slug(self, value):
        return validations.validate_slug(value, instance=self.instance)

    def validate_price(self, value):
        return validations.validate_price(value)

    def validate_image(self, image):
        validations.validate_image(image)
        return image

    def validate(self, data):
        return validations.validate_product_object(data)

class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']

class ProductReadSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='category.title',
        read_only=True
    )

    class Meta:
        model = Product
        fields = ('title', 'price', 'image', 'category')