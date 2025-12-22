from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random
from decimal import Decimal
from django.utils.text import slugify

from categories.models import Category
from products.models import Product
from comments.models import Comment
from carts.models import Cart, CartItem
from orders.models import Order, OrderItem

fake = Faker()

class Command(BaseCommand):
    help = "Seed fake data"

    def handle(self, *args, **kwargs):
        # --- Users ---
        users = []
        for _ in range(5):
            users.append(
                User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password="password123"
                )
            )

        # --- Categories ---
        categories = []
        for _ in range(5):
            cat_title = fake.unique.word().capitalize()
            categories.append(
                Category.objects.create(
                    title=cat_title,
                    slug=slugify(cat_title),
                    description=fake.sentence(),
                    is_active=True
                )
            )

        # --- Products ---
        products = []
        for _ in range(20):
            title = fake.unique.sentence(nb_words=3)
            products.append(
                Product.objects.create(
                    title=title,
                    slug=slugify(title) + '-' + str(random.randint(1000, 9999)),
                    description=fake.text(),
                    price=Decimal(random.randint(50, 2000)),
                    category=random.choice(categories),
                    stock=random.randint(1, 100)
                )
            )

        # --- Carts, Orders, Comments ---
        for user in users:
            # Cart
            cart = Cart.objects.create(user=user)
            for _ in range(3):
                CartItem.objects.create(
                    cart=cart,
                    product=random.choice(products),
                    quantity=random.randint(1, 3)
                )

            # Order
            order = Order.objects.create(
                user=user,
                full_name=fake.name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                line1=fake.street_address(),
                line2=fake.secondary_address(),
                city=fake.city(),
                district=fake.city_suffix(),
                postal_code=fake.postcode(),
                country="Turkey",
                status="processing",
                payment_method="mock"
            )

            total = 0
            for _ in range(2):
                product = random.choice(products)
                qty = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )
                total += product.price * qty

            order.order_total = total
            order.save()

            # Comment
            product_for_comment = random.choice(products)
            Comment.objects.create(
                user=user,
                product=product_for_comment,
                text=fake.sentence(),
                rating=random.randint(1, 5)
            )

        self.stdout.write(self.style.SUCCESS("Fake dataset created successfully!"))