from rest_framework import serializers
from .models import Comment
from users.serializers import UserSimpleSerializer
from products.serializers import ProductSimpleSerializer


class CommentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        extra_kwargs = {
            'rating': {
                'error_messages': {
                    'min_value': 'Rating must be greater than or equal to 1.',
                    'max_value': 'Rating must be lower than or equal to 5.',
                }
            }
        }

    def validate_text(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError('Comment must have at least 5 characters.')
        return value


class CommentCreateSerializer(CommentBaseSerializer):
    class Meta(CommentBaseSerializer.Meta):
        fields = ['rating', 'text', 'product']


class CommentUpdateSerializer(CommentBaseSerializer):
    class Meta(CommentBaseSerializer.Meta):
        fields = ['rating', 'text']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    product = ProductSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'rating', 'text', 'created_at', 'updated_at', 'user', 'product']
        read_only_fields = ['user', 'created_at', 'updated_at']