from django.test import TestCase
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from orders.models import Order, OrderItem
from payments.services import create_payment
from rest_framework.exceptions import ValidationError

class PaymentServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(
            title='Product 1', slug='product-1', price=100, category=self.category, stock=10
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            line1='Address 1',
            city='City',
            district='District',
            postal_code='12345',
            country='Country',
            order_total=100
        )

    def test_create_payment_success(self):
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1, price=100)
        result = create_payment(self.user, self.order)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['order_id'], self.order.id)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'processing')
        self.assertEqual(self.order.payment_method, 'mock')

    def test_create_payment_no_items(self):
        with self.assertRaises(ValidationError):
            create_payment(self.user, self.order)