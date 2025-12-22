from rest_framework.viewsets import ModelViewSet
from django.db.models import RestrictedError
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Category
from . import serializers
from core.permissions import IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="List Categories",
        description="Returns a list of active categories. Admin users can see all categories (including inactive ones).",
        tags=["Categories"],
    ),
    retrieve=extend_schema(
        summary="Retrieve Category Detail",
        description="Returns detailed information for a specific category by ID. Only active categories are accessible to non-admin users.",
        tags=["Categories"],
    ),
    create=extend_schema(
        summary="Create Category (Admin)",
        description="Creates a new category. Only accessible to admin users.",
        tags=["Categories"],
    ),
    update=extend_schema(
        summary="Update Category (Admin)",
        description="Fully updates an existing category. Only accessible to admin users.",
        tags=["Categories"],
    ),
    partial_update=extend_schema(
        summary="Partial Update Category (Admin)",
        description="Partially updates an existing category (e.g., name, is_active). Only accessible to admin users.",
        tags=["Categories"],
    ),
    destroy=extend_schema(
        summary="Delete Category (Admin)",
        description="Deletes a category if it has no related products. "
                    "If there are related products, returns a 400 error with an explanatory message. "
                    "Only accessible to admin users.",
        tags=["Categories"],
        responses={
            204: None,
            400: {'type': 'object', 'properties': {'message': {'type': 'string'}}},
        },
    ),
)
class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Category.objects.all()
        return Category.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CategoryListSerializer
        if self.action == 'retrieve':
            return serializers.CategoryDetailSerializer
        return serializers.CategoryWriteSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RestrictedError:
            return Response(
                {'message': 'Delete the related products before deleting this category.'},
                status=status.HTTP_400_BAD_REQUEST
            )