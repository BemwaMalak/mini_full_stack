from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.error_codes import ERROR_CODES

from .serializers import UserSerializer

UserModel = get_user_model()


class LoginApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("login")
        cls.username = "testuser"
        cls.password = "testpassword"
        cls.email = "test@gmail.com"
        cls.user = UserModel.objects.create_user(
            username=cls.username,
            password=cls.password,
            email=cls.email,
            role=UserModel.Role.USER,
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
        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(self.url, data, format="json")

        # Serialize the user data
        user_data = UserSerializer(self.user).data

        expected_response = {
            "code": ERROR_CODES["LOGIN_SUCCESS"],
            "data": user_data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        data = {
            "username": self.username,
            "password": "wrongpassword",
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["INVALID_CREDENTIALS"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_missing_data(self):
        """
        Test login with missing data (username or password)
        """
        data = {
            "username": self.username,
        }

        response = self.client.post(self.url, data, format="json")

        # Include the validation errors from the response
        expected_response = {
            "code": ERROR_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_empty_username(self):
        """
        Test login with empty username
        """
        data = {
            "username": "",
            "password": self.password,
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_empty_password(self):
        """
        Test login with empty password
        """
        data = {
            "username": self.username,
            "password": "",
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_inactive_user(self):
        """
        Test login with an inactive user account
        """
        self.user.is_active = False
        self.user.save()

        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["INVALID_CREDENTIALS"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_case_insensitive_username(self):
        """
        Test login where username case does not match
        """
        data = {
            "username": self.username.upper(),
            "password": self.password,
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["INVALID_CREDENTIALS"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_sql_injection(self):
        """
        Test login attempt with SQL injection attack in username
        """
        data = {
            "username": "' OR '1'='1",
            "password": "any_password",
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["INVALID_CREDENTIALS"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), expected_response)

    def test_account_lockout_after_failed_attempts(self):
        """
        Test that account is locked after a certain number of failed login attempts
        """
        data = {
            "username": self.username,
            "password": "wrongpassword",
        }

        max_attempts = 5
        for _ in range(max_attempts):
            response = self.client.post(self.url, data, format="json")
            expected_response = {
                "code": ERROR_CODES["INVALID_CREDENTIALS"],
                "data": None,
            }
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.json(), expected_response)

        # Now, even with correct credentials, the account should be locked
        data["password"] = self.password
        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["ACCOUNT_LOCKED"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_nonexistent_user(self):
        """
        Test login attempt with a username that does not exist
        """
        data = {
            "username": "nonexistentuser",
            "password": "any_password",
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": ERROR_CODES["INVALID_CREDENTIALS"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), expected_response)


class LogoutApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("logout")
        cls.username = "testuser"
        cls.password = "testpassword"
        cls.email = "test@gmail.com"
        cls.user = UserModel.objects.create_user(
            username=cls.username,
            password=cls.password,
            email=cls.email,
            role=UserModel.Role.USER,
        )

    def setUp(self):
        # Ensure the user is logged in at the start of each test
        self.client.login(username=self.username, password=self.password)

    def test_logout_authenticated_user(self):
        """
        Test logout with an authenticated user
        """
        response = self.client.post(self.url)

        expected_response = {
            "code": ERROR_CODES["LOGOUT_SUCCESS"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_logout_unauthenticated_user(self):
        """
        Test logout attempt by an unauthenticated user
        """
        self.client.logout()

        response = self.client.post(self.url)

        expected_response = {
            "code": ERROR_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)
