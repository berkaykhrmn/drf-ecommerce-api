from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from categories.models import Category
from comments.models import Comment
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Password123!")
        self.category = Category.objects.create(title="Test Category", slug="test-category")
        self.product = Product.objects.create(
            title="Test Product",
            slug="test-product",
            price=100,
            category=self.category,
            is_active=True,
            stock=10
        )

    def test_create_comment_valid(self):
        comment = Comment.objects.create(product=self.product, user=self.user, rating=4, text="Great product!")
        self.assertEqual(comment.rating, 4)
        self.assertEqual(comment.text, "Great product!")
        self.assertEqual(comment.product, self.product)
        self.assertEqual(comment.user, self.user)
        self.assertTrue(str(comment.rating) in str(comment))
        self.assertTrue(self.product.title in str(comment))
        self.assertTrue(self.user.username in str(comment))

    def test_rating_validation(self):
        with self.assertRaises(ValidationError):
            comment = Comment(product=self.product, user=self.user, rating=6)
            comment.full_clean()

        with self.assertRaises(ValidationError):
            comment = Comment(product=self.product, user=self.user, rating=0)
            comment.full_clean()

    def test_unique_together_constraint(self):
        Comment.objects.create(product=self.product, user=self.user, rating=5)
        with self.assertRaises(IntegrityError):
            Comment.objects.create(product=self.product, user=self.user, rating=3)