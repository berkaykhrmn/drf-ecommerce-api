from django.test import TestCase
from products.models import Product
from categories.models import Category
from django.db.utils import IntegrityError

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category", slug="test-category")

    def test_create_product(self):
        product = Product.objects.create(
            title="Test Product",
            slug="test-product",
            price=100,
            category=self.category,
            stock=10,
            is_active=True
        )
        self.assertEqual(product.title, "Test Product")
        self.assertEqual(product.slug, "test-product")
        self.assertEqual(product.price, 100)
        self.assertEqual(product.stock, 10)
        self.assertTrue(product.is_active)
        self.assertEqual(product.category, self.category)
        self.assertEqual(str(product), "Test Product")

    def test_slug_unique_constraint(self):
        Product.objects.create(
            title="Test Product 1",
            slug="test-product",
            price=50,
            category=self.category
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                title="Test Product 2",
                slug="test-product",
                price=60,
                category=self.category
            )

    def test_stock_default(self):
        product = Product.objects.create(
            title="Test Product 2",
            slug="test-product-2",
            price=50,
            category=self.category
        )
        self.assertEqual(product.stock, 0)

    def test_is_active_default(self):
        product = Product.objects.create(
            title="Test Product 3",
            slug="test-product-3",
            price=70,
            category=self.category
        )
        self.assertTrue(product.is_active)