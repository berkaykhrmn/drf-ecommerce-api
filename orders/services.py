from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Order, OrderItem
from products.services import check_product_stock, decrease_product_stock

@transaction.atomic
def create_order_from_cart(user, cart, address_data):
    cart_items = cart.items.select_related("product").all()
    if not cart_items:
        raise ValidationError("Your cart is empty.")

    order = Order.objects.create(
        user=user,
        full_name=address_data.get("full_name"),
        email=address_data.get("email"),
        phone_number=address_data.get("phone_number"),
        line1=address_data.get("line1"),
        line2=address_data.get("line2"),
        city=address_data.get("city"),
        district=address_data.get("district"),
        postal_code=address_data.get("postal_code"),
        country=address_data.get("country"),
        payment_method="mock"
    )

    for item in cart_items:
        check_product_stock(item.product, item.quantity)
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        decrease_product_stock(item.product, item.quantity)

    total = sum([oi.quantity * oi.price for oi in order.items.all()])
    order.order_total = total
    order.save()

    cart.items.all().delete()

    return order