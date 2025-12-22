from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from .models import Product
from .serializers import ProductReadSerializer, ProductWriteSerializer
from .filters import ProductFilter
from core.permissions import IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="List Products",
        description="Returns detailed information for products.",
        tags=["Products"],
    ),
    retrieve=extend_schema(
        summary="Retrieve Product Detail",
        description="Returns detailed information for a specific product by ID.",
        tags=["Products"],
    ),
    create=extend_schema(
        summary="Create Product (Admin)",
        description="Creates a new product. Only accessible to admin users.",
        tags=["Products"],
    ),
    update=extend_schema(
        summary="Update Product (Admin)",
        description="Fully updates an existing product. Only accessible to admin users.",
        tags=["Products"],
    ),
    partial_update=extend_schema(
        summary="Partial Update Product (Admin)",
        description="Partially updates an existing product. Only accessible to admin users.",
        tags=["Products"],
    ),
    destroy=extend_schema(
        summary="Delete Product (Admin)",
        description="Deletes a product. Only accessible to admin users.",
        tags=["Products"],
    ),
)
class ProductViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ProductReadSerializer
        return ProductWriteSerializer