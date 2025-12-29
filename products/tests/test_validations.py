from django.test import TestCase
from rest_framework import serializers
from products import validations
from products.models import Product
from categories.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductValidationsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            title="Test Product",
            slug="test-slug",
            price=100,
            category=self.category,
            is_active=True,
            stock=10
        )

    def test_validate_title(self):
        self.assertEqual(validations.validate_title("Valid Title"), "Valid Title")
        with self.assertRaises(serializers.ValidationError):
            validations.validate_title("Hi")
        with self.assertRaises(serializers.ValidationError):
            validations.validate_title("A"*101)

    def test_validate_slug(self):
        self.assertEqual(validations.validate_slug("unique-slug"), "unique-slug")
        with self.assertRaises(serializers.ValidationError):
            validations.validate_slug("test-slug")

    def test_validate_price(self):
        self.assertEqual(validations.validate_price(100), 100)
        with self.assertRaises(serializers.ValidationError):
            validations.validate_price(0)
        with self.assertRaises(serializers.ValidationError):
            validations.validate_price(-5)

    def test_validate_product_object(self):
        data = {
            "title": "Long Long Long Title",
            "description": "Description",
            "stock": 5,
            "is_active": True
        }
        self.assertEqual(validations.validate_product_object(data), data)

        data2 = {
            "title": "Short",
            "description": "",
            "stock": 5,
            "is_active": True
        }
        with self.assertRaises(serializers.ValidationError):
            validations.validate_product_object(data2)

        data3 = {
            "title": "Valid Title",
            "description": "",
            "stock": 0,
            "is_active": True
        }
        with self.assertRaises(serializers.ValidationError):
            validations.validate_product_object(data3)

        data4 = {
            "title": "Valid Title Here",
            "description": "",
            "stock": 0,
            "is_active": False
        }
        self.assertEqual(validations.validate_product_object(data4), data4)

    def test_validate_image(self):
        img = SimpleUploadedFile("test.jpg", b"file_content")
        self.assertIsNone(validations.validate_image(img))

        img2 = SimpleUploadedFile("test.txt", b"file_content")
        with self.assertRaises(serializers.ValidationError):
            validations.validate_image(img2)

        class BigFile:
            name = "big.jpg"
            size = 11 * 1024 * 1024

        with self.assertRaises(serializers.ValidationError):
            validations.validate_image(BigFile())