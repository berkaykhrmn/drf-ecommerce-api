from rest_framework.exceptions import ValidationError, NotFound
from .models import Product
from django.db import transaction

def check_product_stock(product, quantity):
    if quantity <= 0:
        raise ValidationError('Quantity must be greater than zero.')

    if quantity > product.stock:
        raise ValidationError(
            f'Only {product.stock} item(s) left in stock.'
        )

def decrease_product_stock(product, quantity):
    with transaction.atomic():
        product.stock -= quantity
        product.save(update_fields=['stock'])

def get_product_or_404(product_id):
    try:
        return Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise NotFound(f'Product with id {product_id} was not found.')