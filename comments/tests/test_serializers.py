from django.test import TestCase
from comments.serializers import CommentCreateSerializer, CommentUpdateSerializer, CommentSerializer
from comments.models import Comment
from django.contrib.auth.models import User
from products.models import Product
from categories.models import Category

class CommentSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            price=100,
            category=self.category,
            is_active=True,
            stock=10
        )

    def test_comment_create_serializer_valid(self):
        data = {'rating': 4, 'text': 'Great product!', 'product': self.product.id}
        serializer = CommentCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        comment = serializer.save(user=self.user)
        self.assertEqual(comment.rating, 4)
        self.assertEqual(comment.text, 'Great product!')

    def test_comment_create_serializer_invalid_rating(self):
        data = {'rating': 6, 'text': 'Nice', 'product': self.product.id}
        serializer = CommentCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('rating', serializer.errors)

    def test_comment_create_serializer_short_text(self):
        data = {'rating': 3, 'text': 'Hi', 'product': self.product.id}
        serializer = CommentCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)

    def test_comment_update_serializer(self):
        comment = Comment.objects.create(product=self.product, user=self.user, rating=5, text='Excellent!')
        data = {'rating': 4, 'text': 'Good product'}
        serializer = CommentUpdateSerializer(comment, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_comment = serializer.save()
        self.assertEqual(updated_comment.rating, 4)
        self.assertEqual(updated_comment.text, 'Good product')

    def test_comment_serializer_nested(self):
        comment = Comment.objects.create(product=self.product, user=self.user, rating=5, text='Excellent!')
        serializer = CommentSerializer(comment)
        data = serializer.data
        self.assertEqual(data['user']['username'], 'testuser')
        self.assertEqual(data['product']['title'], 'Test Product')