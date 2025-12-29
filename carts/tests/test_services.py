from django.test import TestCase
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from carts.models import Cart
from carts.services import get_cart_or_create, add_product_to_cart, update_cart_item, delete_cart_item, clear_cart
from rest_framework.exceptions import NotFound

class CartServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(title='Product 1', slug='product-1', price=100,
                                              category=self.category, stock=10, is_active=True)

    def test_get_cart_or_create(self):
        cart = get_cart_or_create(self.user)
        self.assertIsInstance(cart, Cart)
        cart2 = get_cart_or_create(self.user)
        self.assertEqual(cart.id, cart2.id)

    def test_add_product_to_cart_new_item(self):
        cart = add_product_to_cart(self.user, self.product.id, 2)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_add_product_to_cart_increment_quantity(self):
        add_product_to_cart(self.user, self.product.id, 2)
        cart = add_product_to_cart(self.user, self.product.id, 3)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 5)

    def test_update_cart_item_quantity(self):
        cart = add_product_to_cart(self.user, self.product.id, 2)
        cart_item = cart.items.first()
        updated_cart = update_cart_item(self.user, cart_item.id, 4)
        self.assertEqual(updated_cart.items.first().quantity, 4)

    def test_update_cart_item_delete(self):
        cart = add_product_to_cart(self.user, self.product.id, 2)
        cart_item = cart.items.first()
        updated_cart = update_cart_item(self.user, cart_item.id, 0)
        self.assertEqual(updated_cart.items.count(), 0)

    def test_delete_cart_item(self):
        cart = add_product_to_cart(self.user, self.product.id, 2)
        cart_item = cart.items.first()
        updated_cart = delete_cart_item(self.user, cart_item.id)
        self.assertEqual(updated_cart.items.count(), 0)

    def test_delete_cart_item_not_found(self):
        with self.assertRaises(NotFound):
            delete_cart_item(self.user, 999)

    def test_clear_cart(self):
        add_product_to_cart(self.user, self.product.id, 2)
        cart = clear_cart(self.user)
        self.assertEqual(cart.items.count(), 0)