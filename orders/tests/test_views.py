from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from carts.models import Cart, CartItem
from orders.models import Order
from django.urls import reverse

class OrderViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.admin = User.objects.create_superuser(username='admin', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(
            title='Test Product', slug='test-product', price=100,
            category=self.category, stock=10, is_active=True
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

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

    def test_create_order_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order_create')
        response = self.client.post(url, self.address_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_empty_cart(self):
        self.client.force_authenticate(user=self.user)
        self.cart.items.all().delete()
        url = reverse('order_create')
        response = self.client.post(url, self.address_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_my_orders(self):
        self.client.force_authenticate(user=self.user)
        Order.objects.create(
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
        url = reverse('order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_order_detail_view(self):
        self.client.force_authenticate(user=self.user)
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
        url = reverse('order_detail', args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order.id)