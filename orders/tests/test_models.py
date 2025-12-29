from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from categories.models import Category
from orders.models import Order, OrderItem

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product1 = Product.objects.create(
            title='Test Product 1', slug='test-product-1', price=100,
            category=self.category, stock=10, is_active=True
        )
        self.product2 = Product.objects.create(
            title='Test Product 2', slug='test-product-2', price=50,
            category=self.category, stock=5, is_active=True
        )

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            line1='Address Line 1',
            city='City',
            district='District',
            postal_code='12345',
            country='Country'
        )
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.payment_method, 'mock')
        self.assertEqual(order.order_total, 0)
        self.assertEqual(str(order), f"Order #{order.id} by {self.user.username}")

    def test_orderitem_default_price_and_get_item_total(self):
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            line1='Address Line 1',
            city='City',
            district='District',
            postal_code='12345',
            country='Country'
        )
        item = OrderItem.objects.create(order=order, product=self.product1, quantity=3)
        self.assertEqual(item.price, self.product1.price)
        self.assertEqual(item.get_item_total(), 300)

    def test_calculate_order_total(self):
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            line1='Address Line 1',
            city='City',
            district='District',
            postal_code='12345',
            country='Country'
        )
        OrderItem.objects.create(order=order, product=self.product1, quantity=2)
        OrderItem.objects.create(order=order, product=self.product2, quantity=4)
        total = order.calculate_total()
        self.assertEqual(total, 2*100 + 4*50)
        self.assertEqual(order.order_total, total)

    def test_orderitem_str_method(self):
        order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            line1='Address Line 1',
            city='City',
            district='District',
            postal_code='12345',
            country='Country'
        )
        item = OrderItem.objects.create(order=order, product=self.product1, quantity=3)
        self.assertEqual(str(item), f"{self.product1.title} x 3")