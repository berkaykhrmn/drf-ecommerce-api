from django.test import TestCase
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer, AddToCartSerializer, CartItemUpdateSerializer

class CartSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product1 = Product.objects.create(title='Product 1', slug='product-1', price=100, category=self.category, stock=10)
        self.product2 = Product.objects.create(title='Product 2', slug='product-2', price=50, category=self.category, stock=5)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

    def test_cart_serializer(self):
        serializer = CartSerializer(self.cart)
        data = serializer.data
        self.assertEqual(data['user'], self.user.username)
        self.assertEqual(data['cart_total'], 2*100 + 1*50)
        self.assertEqual(len(data['items']), 2)

    def test_cart_item_serializer(self):
        serializer = CartItemSerializer(self.cart_item1)
        data = serializer.data
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['item_total'], 200)
        self.assertEqual(data['product']['title'], 'Product 1')

    def test_add_to_cart_serializer_valid(self):
        data = {'product_id': self.product1.id, 'quantity': 3}
        serializer = AddToCartSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_add_to_cart_serializer_invalid(self):
        data = {'product_id': self.product1.id, 'quantity': 0}  # min_value=1
        serializer = AddToCartSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_cart_item_update_serializer_valid(self):
        data = {'quantity': 5}
        serializer = CartItemUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_cart_item_update_serializer_invalid(self):
        data = {'quantity': -1}
        serializer = CartItemUpdateSerializer(data=data)
        self.assertFalse(serializer.is_valid())