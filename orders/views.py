from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from . import serializers as order_serializers
from carts.services import get_cart_or_create
from .services import create_order_from_cart
from .models import Order
from payments.services import create_payment

class MockPaymentSerializer(serializers.Serializer):
    pass

@extend_schema_view(
    post=extend_schema(
        summary="Create Order",
        description="Creates a new order from the authenticated user's current cart. "
                    "Requires shipping/billing address data. "
                    "Upon success, the cart is cleared and an order with 'pending' status is created.",
        tags=["Orders"],
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
)
class CreateOrderView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = order_serializers.OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address_data = serializer.validated_data
        cart = get_cart_or_create(request.user)
        try:
            order = create_order_from_cart(request.user, cart, address_data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Unexpected Error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Order created', 'order_id': order.id}, status=status.HTTP_201_CREATED)

@extend_schema_view(
    get=extend_schema(
        summary="List My Orders",
        description="Returns a list of orders belonging to the authenticated user.",
        tags=["Orders"],
    )
)
class OrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = order_serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@extend_schema_view(
    get=extend_schema(
        summary="List All Orders (Admin)",
        description="Returns a list of all orders in the system. "
                    "Admin only. Optional query parameter: ?userId=<id> to filter by user.",
        tags=["Orders"],
    )
)
class AdminOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = order_serializers.OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        user_id = self.request.query_params.get("userId")
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return queryset

@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Order Detail (Admin)",
        description="Retrieves detailed information for any order by ID. Admin only.",
        tags=["Orders"],
    ),
    put=extend_schema(
        summary="Update Order Status (Admin)",
        description="Fully updates an order (typically used for status changes). Admin only.",
        tags=["Orders"],
    ),
    patch=extend_schema(
        summary="Partial Update Order Status (Admin)",
        description="Partially updates an order (e.g., change status to 'shipped', 'processing'). Admin only.",
        tags=["Orders"],
    ),
)
class AdminOrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = order_serializers.OrderSerializer
    lookup_url_kwarg = "order_id"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return order_serializers.OrderStatusUpdateSerializer
        return order_serializers.OrderSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Retrieve My Order Detail",
        description="Returns detailed information for a specific order belonging to the authenticated user.",
        tags=["Orders"],
    )
)
class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = order_serializers.OrderSerializer
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@extend_schema(
    summary="Process Mock Payment",
    description="Simulates payment processing for a pending order. "
                "Only works on orders with 'pending' status and belonging to the authenticated user. "
                "Upon success, updates order status accordingly (e.g., to 'processing').",
    tags=["Orders"],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)
class MockPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MockPaymentSerializer

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "pending":
            return Response({"error": "Payment already processed or order not pending"}, status=status.HTTP_400_BAD_REQUEST)

        payment_result = create_payment(request.user, order)
        return Response(payment_result, status=status.HTTP_200_OK)