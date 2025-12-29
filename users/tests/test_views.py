from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/user/register/'

    def test_user_registration_successful(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'Password123!',
            'password_confirm': 'Password123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_failed_when_passwords_dont_match(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'Password123!',
            'password_confirm': '!123Password',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_failed_with_duplicate_email(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password123!',
        )
        data = {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password': 'Password123!',
            'password_confirm': 'Password123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.login_url = '/api/user/login/'
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password123!',
        )
        
    def test_user_login_successful(self):
        data = {
            'username': 'testuser',
            'password': 'Password123!',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_login_failed_with_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': '!123Password',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_failed_with_missing_fields(self):
        data = {
            'username': 'testuser',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LogoutViewTests(APITestCase):
    def setUp(self):
        self.logout_url = '/api/user/logout/'
        self.user = User.objects.create_user(
            username='testuser',
            password='Password123!',
        )

    def test_user_logout_successful(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
    def test_user_logout_failed_for_unauthenticated_user(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserUpdateViewTests(APITestCase):
    def setUp(self):
        self.update_url = '/api/user/update/'
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password123!',
        )

    def test_unauthenticated_user_cannot_update(self):
        response = self.client.put(self.update_url, {
            'username': 'hacker',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update_successful(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser2')
        self.assertEqual(self.user.email, 'testuser2@example.com')

    def test_user_partially_update_successful(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'first_name': 'test',
        }
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'test')

class ChangePasswordViewTests(APITestCase):
    def setUp(self):
        self.change_password_url = '/api/user/change-password/'
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password123!',
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_unauthenticated_user_cannot_change_password(self):
        self.client.credentials()
        response = self.client.post(self.change_password_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_change_password_successful(self):
        data = {
            'old_password': 'Password123!',
            'new_password': '!123Password',
            'new_password_confirm': '!123Password',
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('!123Password'))

    def test_user_change_password_failed_with_wrong_password(self):
        data = {
            'old_password': '!123Password',
            'new_password': 'Password123!',
            'new_password_confirm': 'Password123!',
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Password123!'))

    def test_user_change_password_failed_when_passwords_dont_match(self):
        data = {
            'old_password': 'Password123!',
            'new_password': '!123Password',
            'new_password_confirm': 'Password123!',
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_change_password_failed_with_weak_password(self):
        data = {
            'old_password': 'Password123!',
            'new_password': '123',
            'new_password_confirm': '123',
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)