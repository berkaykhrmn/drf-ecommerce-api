from .serializers import APIRootSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema

@extend_schema(
    operation_id="api_root",
    summary="API Root",
    description="This endpoint provides a guide to all main endpoints in the project.",
    tags=["Root"],
    responses=APIRootSerializer
)
@api_view(['GET'])
def api_root(request, fmt=None):
    return Response({
        'products': reverse('product-list', request=request, format=fmt),
        'categories': reverse('category-list', request=request, format=fmt),
        'comments': reverse('comment-list', request=request, format=fmt),
        'cart': {
            'detail': reverse('cart_detail', request=request, format=fmt),
            'add_item': reverse('cart_add', request=request, format=fmt),
            'clear': reverse('cart_clear', request=request, format=fmt),
        },
        'orders': {
            'user_orders': reverse('order_list', request=request, format=fmt),
            'create_order': reverse('order_create', request=request, format=fmt),
            'payment': reverse('mock_payment', kwargs={'order_id': 1}, request=request, format=fmt),
            'admin_orders': reverse('admin_order_list', request=request, format=fmt),
        },
        'user': {
            'register': reverse('user_register', request=request, format=fmt),
            'login': reverse('user_login', request=request, format=fmt),
            'update': reverse('user_update', request=request, format=fmt),
            'change_password': reverse('user_change_password', request=request, format=fmt),
        }
    })