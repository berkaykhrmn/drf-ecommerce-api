import os
from rest_framework import serializers
from .models import Product

def validate_title(value):
    if len(value) < 3:
        raise serializers.ValidationError('This field is too short')
    if len(value) > 100:
        raise serializers.ValidationError('This field is too long')
    return value

def validate_slug(value, instance=None):
    product_id = instance.id if instance else None
    if Product.objects.filter(slug=value).exclude(id=product_id).exists():
        raise serializers.ValidationError('This field is taken')
    return value

def validate_price(value):
    if value < 1:
        raise serializers.ValidationError('Price must be greater than 0')
    return value

def validate_product_object(data):
    title = data.get('title', '')
    description = data.get('description', '')
    stock = data.get('stock')
    is_active = data.get('is_active')

    if not description and len(title) < 10:
        raise serializers.ValidationError(
            'If there is no description, the title must be at least 10 characters long'
        )

    if is_active and (stock is None or stock == 0):
        raise serializers.ValidationError(
            'Active product stock cannot be zero'
        )

    return data


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE_MB = 10

def validate_image(file):
    ext = os.path.splitext(file.name)[1].lower().lstrip('.')

    if ext not in ALLOWED_EXTENSIONS:
        raise serializers.ValidationError('Image must be .png, .jpg, .jpeg')

    file_size_mb = file.size/ (1024*1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise serializers.ValidationError('Image size is too big. Maximum 10MB.')