from django.test import TestCase
from products.models import Product
from products.serializers import ProductReadSerializer, ProductWriteSerializer
from categories.models import Category

class ProductReadSerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')

    def test_read_serializer(self):
        product = Product.objects.create(
            title='Test Product',
            slug='test-slug',
            price=1500,
            category=self.category,
            is_active=True,
            stock=10
        )
        serializer = ProductReadSerializer(product)
        data = serializer.data

        expected_fields = ['title', 'slug', 'price', 'is_active', 'category', 'image']
        for field in expected_fields:
            self.assertIn(field, data)
        self.assertEqual(data['category'], 'Test Category')

class ProductWriteSerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')

    def test_valid_data_create_product(self):
        data = {
            'title': 'Test Product',
            'slug': 'test-slug',
            'price': 1500,
            'category': self.category.id,
            'is_active': True,
            'stock': 10
        }
        serializer = ProductWriteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.title, 'Test Product')