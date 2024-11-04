from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .enums import Message

UserModel = get_user_model()


class LoginApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testuser"
        cls.password = "testpassword"
        cls.user = UserModel.objects.create_user(
            username=cls.username, password=cls.password, role=UserModel.Role.USER
        )

    def setUp(self):
        # Reset failed_login_attempts and is_locked before each test
        self.user.failed_login_attempts = 0
        self.user.is_locked = False
        self.user.save()

    def test_successful_login(self):
        """
        Test login with valid credentials
        """
        url = reverse("login")
        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], Message.LOGIN_SUCCESS.value)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["username"], self.username)

    def test_login_with_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        url = reverse("login")
        data = {
            "username": self.username,
            "password": "wrongpassword",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], Message.INVALID_CREDENTIALS.value)
        self.assertIsNone(response.data.get("data"))

    def test_login_with_missing_data(self):
        """
        Test login with missing data (username or password)
        """
        url = reverse("login")
        data = {
            "username": self.username,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Message.VALIDATION_ERROR.value)
        self.assertIn("password", response.data["data"])

    def test_login_with_empty_username(self):
        """
        Test login with empty username
        """
        url = reverse("login")
        data = {
            "username": "",
            "password": self.password,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Message.VALIDATION_ERROR.value)
        self.assertIn("username", response.data["data"])

    def test_login_with_empty_password(self):
        """
        Test login with empty password
        """
        url = reverse("login")
        data = {
            "username": self.username,
            "password": "",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Message.VALIDATION_ERROR.value)
        self.assertIn("password", response.data["data"])

    def test_login_with_inactive_user(self):
        """
        Test login with an inactive user account
        """
        self.user.is_active = False
        self.user.save()

        url = reverse("login")
        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], Message.INVALID_CREDENTIALS.value)
        self.assertIsNone(response.data.get("data"))

    def test_login_with_case_insensitive_username(self):
        """
        Test login where username case does not match
        """
        url = reverse("login")
        data = {
            "username": self.username.upper(),
            "password": self.password,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], Message.INVALID_CREDENTIALS.value)

    def test_login_with_sql_injection(self):
        """
        Test login attempt with SQL injection attack in username
        """
        url = reverse("login")
        data = {
            "username": "' OR '1'='1",
            "password": "any_password",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], Message.INVALID_CREDENTIALS.value)
        self.assertIsNone(response.data.get("data"))

    def test_account_lockout_after_failed_attempts(self):
        """
        Test that account is locked after a certain number of failed login attempts
        """
        url = reverse("login")
        data = {
            "username": self.username,
            "password": "wrongpassword",
        }

        max_attempts = 5
        for _ in range(max_attempts):
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(
                response.data["message"], Message.INVALID_CREDENTIALS.value
            )

        # Now, even with correct credentials, the account should be locked
        data["password"] = self.password
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], Message.ACCOUNT_LOCKED.value)
        self.assertIsNone(response.data.get("data"))

    def test_login_with_nonexistent_user(self):
        """
        Test login attempt with a username that does not exist
        """
        url = reverse("login")
        data = {
            "username": "nonexistentuser",
            "password": "any_password",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], Message.INVALID_CREDENTIALS.value)
        self.assertIsNone(response.data.get("data"))

    def test_login_with_special_characters_in_username(self):
        """
        Test login with special characters in username
        """
        special_username = "user!@#"
        UserModel.objects.create_user(
            username=special_username, password=self.password, role=UserModel.Role.USER
        )

        url = reverse("login")
        data = {
            "username": special_username,
            "password": self.password,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], Message.LOGIN_SUCCESS.value)
        self.assertEqual(response.data["data"]["username"], special_username)
