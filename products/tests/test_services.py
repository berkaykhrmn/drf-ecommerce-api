from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from products.models import Product
from categories.models import Category
from products import services

class ProductServicesTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            title="Test Product",
            slug="test-product",
            price=100,
            category=self.category,
            is_active=True,
            stock=10
        )

    def test_check_product_stock(self):
        try:
            services.check_product_stock(self.product, 5)
        except ValidationError:
            self.fail("check_product_stock validation error")

    def test_check_product_stock_zero_or_less(self):
        with self.assertRaises(ValidationError) as context:
            services.check_product_stock(self.product, 0)
        self.assertIn("Quantity must be greater than zero", str(context.exception))

        with self.assertRaises(ValidationError):
            services.check_product_stock(self.product, -3)

    def test_check_product_stock_exceeds(self):
        with self.assertRaises(ValidationError) as context:
            services.check_product_stock(self.product, 20)
        self.assertIn(f'Only {self.product.stock} item(s) left in stock.', str(context.exception))

    def test_decrease_product_stock(self):
        services.decrease_product_stock(self.product, 4)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 6)

    def test_get_product_or_404_exists(self):
        product = services.get_product_or_404(self.product.id)
        self.assertEqual(product.id, self.product.id)

    def test_get_product_or_404_not_found(self):
        with self.assertRaises(NotFound) as context:
            services.get_product_or_404(9999)
        self.assertIn('Product with id 9999 was not found.', str(context.exception))

