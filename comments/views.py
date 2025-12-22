from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer
from core.permissions import IsOwnerOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="List Comments",
        description="Returns a list of all approved/active comments. "
                    "Read-only for unauthenticated users.",
        tags=["Comments"],
    ),
    retrieve=extend_schema(
        summary="Retrieve Comment Detail",
        description="Returns detailed information for a specific comment by ID.",
        tags=["Comments"],
    ),
    create=extend_schema(
        summary="Create Comment",
        description="Allows authenticated users to add a new comment to a product. "
                    "The comment is associated with the logged-in user.",
        tags=["Comments"],
    ),
    update=extend_schema(
        summary="Update Comment (Owner Only)",
        description="Fully updates an existing comment. Only the owner of the comment can perform this action.",
        tags=["Comments"],
    ),
    partial_update=extend_schema(
        summary="Partial Update Comment (Owner Only)",
        description="Partially updates an existing comment (e.g., text or rating). Only the owner can perform this action.",
        tags=["Comments"],
    ),
    destroy=extend_schema(
        summary="Delete Comment (Owner Only)",
        description="Deletes a comment. Only the owner of the comment can perform this action.",
        tags=["Comments"],
    ),
)
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user', 'product')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)