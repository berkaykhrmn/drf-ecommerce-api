from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from . import serializers, services
from core.serializers import EmptySerializer


@extend_schema_view(
    post=extend_schema(
        summary="Add Product to Cart",
        description="Adds a product to the authenticated user's cart. "
                    "If the product is already in the cart, increases its quantity. "
                    "Quantity defaults to 1 if not provided.",
        tags=["Cart"],
    )
)
class AddToCartView(generics.GenericAPIView):
    serializer_class = serializers.AddToCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = services.add_product_to_cart(
            user=request.user,
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data.get("quantity", 1)
        )
        return Response(
            serializers.CartSerializer(cart).data,
            status=status.HTTP_201_CREATED
        )


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Cart",
        description="Returns the full details of the authenticated user's cart. ",
        tags=["Cart"],
    )
)
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return services.get_cart_or_create(self.request.user)


@extend_schema_view(
    put=extend_schema(
        summary="Update Cart Item Quantity",
        description="Updates the quantity of a specific item in the authenticated user's cart. "
                    "Use quantity=0 to remove the item entirely (alternative to delete endpoint).",
        tags=["Cart"],
    )
)
class UpdateCartItemView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = services.update_cart_item(
            user=request.user,
            cart_item_id=pk,
            quantity=serializer.validated_data["quantity"]
        )
        return Response(serializers.CartSerializer(cart).data)


@extend_schema_view(
    delete=extend_schema(
        summary="Remove Item from Cart",
        description="Removes a specific item from the authenticated user's cart by cart item ID.",
        tags=["Cart"],
        responses={200: serializers.CartSerializer},
    )
)
class DeleteCartItemView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        cart = services.delete_cart_item(request.user, pk)
        return Response(serializers.CartSerializer(cart).data)


@extend_schema_view(
    delete=extend_schema(
        summary="Clear Entire Cart",
        description="Removes all items from the authenticated user's cart.",
        tags=["Cart"],
        responses={200: serializers.CartSerializer},
    )
)
class ClearCartView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        cart = services.clear_cart(request.user)
        return Response(serializers.CartSerializer(cart).data)