from django.test import TestCase
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from carts.models import Cart, CartItem
from orders.services import create_order_from_cart
from rest_framework.exceptions import ValidationError

class OrderServiceTests(TestCase):
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
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

        self.address_data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'line1': 'Address Line 1',
            'line2': 'Address Line 2',
            'city': 'City',
            'district': 'District',
            'postal_code': '12345',
            'country': 'Country'
        }

    def test_create_order_from_cart_success(self):
        order = create_order_from_cart(self.user, self.cart, self.address_data)
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.order_total, 2*100 + 1*50)
        self.assertEqual(Product.objects.get(id=self.product1.id).stock, 8)
        self.assertEqual(Product.objects.get(id=self.product2.id).stock, 4)
        self.assertEqual(self.cart.items.count(), 0)

    def test_create_order_from_empty_cart(self):
        user2 = User.objects.create_user(username='emptyuser', password='Password123!')
        empty_cart = Cart.objects.create(user=user2)
        with self.assertRaises(ValidationError):
            create_order_from_cart(user2, empty_cart, self.address_data)

    def test_create_order_exceed_stock(self):
        cart_item = self.cart.items.get(product=self.product1)
        cart_item.quantity = 20
        cart_item.save()
        with self.assertRaises(ValidationError):
            create_order_from_cart(self.user, self.cart, self.address_data)