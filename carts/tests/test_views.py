from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from carts.models import CartItem
from django.urls import reverse

class CartViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(title='Product 1', slug='product-1', price=100, category=self.category, stock=10)
        self.cart_url = reverse('cart_detail')
        self.add_url = reverse('cart_add')
        self.clear_url = reverse('cart_clear')

    def test_add_product_to_cart(self):
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['items'][0]['quantity'], 2)

    def test_retrieve_cart(self):
        self.client.post(self.add_url, {'product_id': self.product.id, 'quantity': 2})
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)

    def test_update_cart_item_quantity(self):
        self.client.post(self.add_url, {'product_id': self.product.id, 'quantity': 2})
        cart_item_id = CartItem.objects.first().id
        response = self.client.put(reverse('cart_item_update', args=[cart_item_id]), {'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items'][0]['quantity'], 5)

    def test_delete_cart_item(self):
        self.client.post(self.add_url, {'product_id': self.product.id, 'quantity': 2})
        cart_item_id = CartItem.objects.first().id
        response = self.client.delete(reverse('cart_item_delete', args=[cart_item_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)

    def test_clear_cart(self):
        self.client.post(self.add_url, {'product_id': self.product.id, 'quantity': 2})
        response = self.client.delete(self.clear_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)