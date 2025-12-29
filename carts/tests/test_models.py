from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from categories.models import Category
from carts.models import Cart, CartItem

class CartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product1 = Product.objects.create(
            title='Product 1', slug='product-1', price=100,
            category=self.category, stock=10, is_active=True
        )
        self.product2 = Product.objects.create(
            title='Product 2', slug='product-2', price=50,
            category=self.category, stock=5, is_active=True
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(str(self.cart), f"{self.user}'s cart")

    def test_add_cart_item_and_total(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)
        self.assertEqual(self.cart.items.count(), 2)
        self.assertEqual(self.cart.get_cart_total(), 2*100 + 1*50)

    def test_unique_cartitem_constraint(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        with self.assertRaises(Exception):
            # Aynı product için duplicate eklenmeye çalışılırsa hata
            CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)