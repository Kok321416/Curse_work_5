from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты для модели пользователя"""

    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_str_method(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )
        self.assertEqual(str(user), "test@example.com")


class UserRegistrationTest(APITestCase):
    """Тесты регистрации пользователя"""

    def test_user_registration_success(self):
        """Тест успешной регистрации"""
        url = reverse("users:register")
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_user_registration_password_mismatch(self):
        """Тест регистрации с несовпадающими паролями"""
        url = reverse("users:register")
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "password_confirm": "differentpass",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        """Тест регистрации с существующим email"""
        User.objects.create_user(
            email="test@example.com", username="existinguser", password="testpass123"
        )

        url = reverse("users:register")
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(APITestCase):
    """Тесты авторизации пользователя"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )

    def test_user_login_success(self):
        """Тест успешной авторизации"""
        url = reverse("users:login")
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_user_login_invalid_credentials(self):
        """Тест авторизации с неверными данными"""
        url = reverse("users:login")
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_missing_data(self):
        """Тест авторизации с отсутствующими данными"""
        url = reverse("users:login")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTest(APITestCase):
    """Тесты профиля пользователя"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_get_profile_authenticated(self):
        """Тест получения профиля авторизованным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_get_profile_unauthenticated(self):
        """Тест получения профиля неавторизованным пользователем"""
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        """Тест обновления профиля"""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        url = reverse("users:profile")
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "telegram_chat_id": "123456789",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.telegram_chat_id, "123456789")
