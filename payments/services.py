from rest_framework.exceptions import ValidationError

def create_payment(user, order, card_data=None):
    if not order.items.exists():
        raise ValidationError("Please select at least one item for payment")

    result = {
        "status": "success",
        "payment_id": f"MOCK-{order.id}",
        "order_id": order.id,
        "amount": float(order.order_total),
        "method": "mock",
        "message": "Payment completed successfully"
    }

    order.payment_method = "mock"
    order.status = "processing"
    order.save()

    return result