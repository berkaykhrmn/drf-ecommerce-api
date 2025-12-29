from django.test import TestCase
from categories.models import Category
from django.db.utils import IntegrityError

class CategoryModelTests(TestCase):
    def test_create_category(self):
        category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            description="All items in this category"
        )
        self.assertEqual(category.title, "Test Category")
        self.assertEqual(category.slug, "test-category")
        self.assertEqual(category.description, "All items in this category")
        self.assertTrue(category.is_active)
        self.assertEqual(str(category), "Test Category")

    def test_title_unique_constraint(self):
        Category.objects.create(title="Test Category", slug="test-category")
        with self.assertRaises(IntegrityError):
            Category.objects.create(title="Test Category", slug="test-category2")

    def test_slug_unique_constraint(self):
        Category.objects.create(title="Test Category", slug="test-category")
        with self.assertRaises(IntegrityError):
            Category.objects.create(title="Another Category", slug="test-category")

    def test_description_optional(self):
        category = Category.objects.create(title="Test Category 2", slug="test-category-2")
        self.assertIsNone(category.description)

    def test_is_active_default(self):
        category = Category.objects.create(title="Test Category 3", slug="test-category-3")
        self.assertTrue(category.is_active)