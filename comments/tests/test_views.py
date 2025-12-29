from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from categories.models import Category
from products.models import Product
from comments.models import Comment

class CommentViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='Password123!')
        self.user2 = User.objects.create_user(username='user2', password='Password123!')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            price=100,
            category=self.category,
            is_active=True,
            stock=10
        )
        self.comment = Comment.objects.create(
            product=self.product,
            user=self.user1,
            rating=4,
            text='Great product!'
        )
        self.list_url = reverse('comment-list')
        self.detail_url = lambda pk: reverse('comment-detail', args=[pk])

    def test_list_comments_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_comment(self):
        url = self.detail_url(self.comment.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Great product!')

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.user2)
        data = {'rating': 5, 'text': 'Awesome!', 'product': self.product.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'Awesome!')

    def test_create_comment_unauthenticated(self):
        data = {'rating': 5, 'text': 'Awesome!', 'product': self.product.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_comment_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url(self.comment.id)
        data = {'rating': 3, 'text': 'Updated text'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Updated text')

    def test_update_comment_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = self.detail_url(self.comment.id)
        data = {'rating': 3, 'text': 'Hack attempt'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url(self.comment.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = self.detail_url(self.comment.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)