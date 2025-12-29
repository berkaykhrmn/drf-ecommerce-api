from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product

class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='Password123!')
        self.user = User.objects.create_user(username='user', password='Password123!')

        self.category_active = Category.objects.create(title="Test Category", slug="test-category", is_active=True)
        self.category_inactive = Category.objects.create(title="Inactive Category", slug="inactive-category", is_active=False)

        self.list_url = reverse('category-list')
        self.detail_url = lambda pk: reverse('category-detail', args=[pk])

    def test_list_categories_public(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [c['title'] for c in response.data['results']]
        self.assertIn("Test Category", titles)
        self.assertNotIn("Inactive Category", titles)

    def test_list_categories_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [c['title'] for c in response.data['results']]
        self.assertIn("Test Category", titles)
        self.assertIn("Inactive Category", titles)

    def test_retrieve_category_active(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.category_active.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Category")

    def test_retrieve_category_inactive_public(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.category_inactive.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'New Category', 'slug': 'new-category', 'is_active': True}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = self.detail_url(self.category_active.id)
        data = {'title': 'Updated Category', 'slug': 'test-category', 'is_active': True}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category_active.refresh_from_db()
        self.assertEqual(self.category_active.title, 'Updated Category')

    def test_delete_category_with_products(self):
        self.client.force_authenticate(user=self.admin)
        Product.objects.create(title="Test Product", slug="test-product", price=100, category=self.category_active, is_active=True, stock=10)
        url = self.detail_url(self.category_active.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Delete the related products', response.data['message'])