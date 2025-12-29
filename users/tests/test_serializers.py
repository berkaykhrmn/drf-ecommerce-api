from django.test import TestCase
from django.contrib.auth.models import User
from users.serializers import RegisterSerializer, LoginSerializer, UserUpdateSerializer, ChangePasswordSerializer
from unittest.mock import patch


class RegisterSerializerTests(TestCase):

    def test_create_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'Password123!',
            'password_confirm': 'Password123!',
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password('Password123!'))

    def test_passwords_dont_match(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Password123!',
            'password_confirm': '!123password',
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_weak_password(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': '123',
            'password_confirm': '123',
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class LoginSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            password='Password123!',
        )

    @patch('users.serializers.authenticate')
    def test_login(self, mock_authenticate):
        mock_authenticate.return_value = self.user
        data = {
            'username': 'testuser',
            'password': 'Password123!',
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIn('access', serializer.validated_data)
        self.assertIn('refresh', serializer.validated_data)
        self.assertEqual(serializer.validated_data['user'], self.user)
        
    @patch('users.serializers.authenticate')
    def test_invalid_login(self, mock_authenticate):
        mock_authenticate.return_value = None
        data = {
            'username': 'testuser',
            'password': '!123Password',
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class UserUpdateSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
        )
        self.user2 = User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
        )

    def test_update_user_with_existing_username(self):
        serializer = UserUpdateSerializer(instance=self.user, data={'username': 'testuser2'})
        self.assertFalse(serializer.is_valid())

class ChangePasswordSerializerTests(TestCase):

    def test_passwords_match(self):
        data = {
            'old_password': 'Password123!',
            'new_password': '!123Password',
            'new_password_confirm': '!123Password',
        }
        serializer = ChangePasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_passwords_dont_match(self):
        data = {
            'old_password': 'Password123!',
            'new_password': '!123Password',
            'new_password_confirm': '123Password',
        }
        serializer = ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())