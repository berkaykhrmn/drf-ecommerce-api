from django.test import TestCase
from categories.models import Category
from categories.serializers import CategoryListSerializer, CategoryWriteSerializer, CategoryDetailSerializer
from products.models import Product

class CategorySerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category", slug="test-category")
        self.product = Product.objects.create(
            title="Test Product",
            slug="test-product",
            price=100,
            category=self.category,
            is_active=True,
            stock=10
        )

    def test_category_list_serializer(self):
        serializer = CategoryListSerializer(self.category)
        data = serializer.data
        self.assertEqual(data['id'], self.category.id)
        self.assertEqual(data['title'], "Test Category")

    def test_category_write_serializer_valid(self):
        data = {
            'title': 'Test Category 2',
            'slug': 'test-category-2',
            'description': 'A description',
            'is_active': True
        }
        serializer = CategoryWriteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.title, 'Test Category 2')

    def test_category_detail_serializer(self):
        serializer = CategoryDetailSerializer(self.category)
        data = serializer.data
        self.assertEqual(data['id'], self.category.id)
        self.assertEqual(data['title'], "Test Category")
        self.assertEqual(len(data['products']), 1)
        self.assertEqual(data['products'][0]['title'], "Test Product")