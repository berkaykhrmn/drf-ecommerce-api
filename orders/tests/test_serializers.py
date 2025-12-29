from django.test import TestCase
from orders.serializers import OrderCreateSerializer, OrderItemSerializer, OrderSerializer
from orders.models import Order, OrderItem
from products.models import Product
from categories.models import Category
from django.contrib.auth.models import User
from decimal import Decimal

class OrderSerializerTests(TestCase):
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
        self.order = Order.objects.create(
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
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )

    def test_order_create_serializer_valid(self):
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'line1': 'Address Line 1',
            'city': 'City',
            'district': 'District',
            'postal_code': '12345',
            'country': 'Country'
        }
        serializer = OrderCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_order_item_serializer(self):
        serializer = OrderItemSerializer(self.order_item)
        data = serializer.data
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(Decimal(data['price']), self.product.price)
        self.assertEqual(data['product']['title'], 'Test Product')

    def test_order_serializer_nested(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        self.assertEqual(data['user'], self.user.username)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['product']['title'], 'Test Product')
        self.assertEqual(data['delivery_address']['full_name'], 'Test User')
        self.assertEqual(data['delivery_address']['email'], 'test@example.com')