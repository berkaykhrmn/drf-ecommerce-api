from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from categories.models import Category


class ProductListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('product-list')
        self.category = Category.objects.create(title="Test Category")
        self.active_product = Product.objects.create(
            title="Active Test Product",
            slug="active-product",
            price=1500,
            category=self.category,
            is_active=True,
            stock=10,
        )
        self.inactive_product = Product.objects.create(
            title="Inactive Test Product",
            slug="inactive-product",
            price=500,
            category=self.category,
            is_active=False,
        )

    def test_list_active_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        active_titles = [p['title'] for p in results if p['is_active']]
        self.assertIn('Active Test Product', active_titles)


class ProductRetrieveViewTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            title="Active Test Product",
            slug="active-product",
            price=1500,
            category=self.category,
            is_active=True,
            stock=10,
        )
        self.url = reverse('product-detail', args=[self.product.id])
        self.not_found_url = reverse('product-detail', args=[9999])

    def test_retrieve_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Active Test Product')
        self.assertIn('price', response.data)

    def test_retrieve_product_not_found(self):
        response = self.client.get(self.not_found_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProductAdminCRUDTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='Password123!')
        self.user = User.objects.create_user(username='user', password='Password123!')
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            title="Original Product",
            slug="original-product",
            price=1500,
            category=self.category,
            is_active=True,
            stock=10,
        )

    def test_admin_create_product(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'New Product',
            'slug': 'new-product',
            'price': 800,
            'category': self.category.id,
            'is_active': True,
            'stock': 5,
        }
        url = reverse('product-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_update_product(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-detail', args=[self.product.id])
        data = {
            'title': 'Updated Product Title',
            'slug': 'original-product',
            'price': 1600,
            'category': self.category.id,
            'is_active': True,
            'stock': 10,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Updated Product Title')

    def test_admin_partial_update_product(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-detail', args=[self.product.id])
        data = {
            'price': 1700,
            'title': self.product.title,
            'slug': self.product.slug,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 1700)

    def test_admin_delete_product(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

class ProductFilterTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category", slug="test-category")
        self.category2 = Category.objects.create(title="Test Category2", slug="test-category2")

        self.product = Product.objects.create(
            title="Test Product",
            slug="test-product",
            price=1500,
            category=self.category,
            is_active=True,
            stock=10,
        )
        self.product2 = Product.objects.create(
            title="Test Product2",
            slug="test-product2",
            price=800,
            category=self.category,
            is_active=True,
            stock=5,
        )
        self.product3 = Product.objects.create(
            title="Test Product3",
            slug="test-product3",
            price=50,
            category=self.category2,
            is_active=True,
            stock=15,
        )
        self.url = reverse('product-list')

    def test_filter_category(self):
        response = self.client.get(self.url, {'category': 'test-category'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [p['title'] for p in response.data['results']]
        self.assertIn('Test Product', titles)
        self.assertIn('Test Product2', titles)
        self.assertNotIn('Test Product3', titles)


    def test_filter_price_range(self):
        response = self.client.get(self.url, {'price__gt' : 100, 'price__lt' : 1400})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [p['title'] for p in response.data['results']]
        self.assertIn('Test Product2', titles)
        self.assertNotIn('Test Product', titles)
        self.assertNotIn('Test Product3', titles)

    def test_search_title(self):
        response = self.client.get(self.url, {'title__icontains': 'Test Product2'})
        self.assertEqual(response.status_code, 200)
        titles = [p['title'] for p in response.data['results']]
        self.assertIn('Test Product2', titles)
        self.assertNotIn('Test Product', titles)
        self.assertNotIn('Test Product3', titles)
