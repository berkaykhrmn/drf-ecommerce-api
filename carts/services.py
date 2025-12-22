from django.db import transaction
from rest_framework.exceptions import NotFound
from products.services import check_product_stock, get_product_or_404
from .models import Cart, CartItem


def get_cart_or_create(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@transaction.atomic
def add_product_to_cart(user, product_id, quantity):
    product = get_product_or_404(product_id)
    check_product_stock(product, quantity)

    cart = get_cart_or_create(user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        cart_item.quantity = quantity
    else:
        new_quantity = cart_item.quantity + quantity
        check_product_stock(product, new_quantity)
        cart_item.quantity = new_quantity

    cart_item.save()
    return cart


@transaction.atomic
def update_cart_item(user, cart_item_id, quantity):
    try:
        cart_item = CartItem.objects.get(
            pk=cart_item_id,
            cart__user=user
        )
    except CartItem.DoesNotExist:
        raise NotFound("Cart item not found")

    if quantity <= 0:
        cart_item.delete()
    else:
        check_product_stock(cart_item.product, quantity)
        cart_item.quantity = quantity
        cart_item.save()

    return cart_item.cart


@transaction.atomic
def delete_cart_item(user, cart_item_id):
    try:
        cart_item = CartItem.objects.get(
            pk=cart_item_id,
            cart__user=user
        )
    except CartItem.DoesNotExist:
        raise NotFound("Cart item not found")

    cart_item.delete()
    return cart_item.cart


@transaction.atomic
def clear_cart(user):
    cart = get_cart_or_create(user)
    cart.items.all().delete()
    return cart