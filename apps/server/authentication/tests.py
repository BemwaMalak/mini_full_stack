from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.response_codes import RESPONSE_CODES

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
            "code": RESPONSE_CODES["LOGIN_SUCCESS"],
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
            "code": RESPONSE_CODES["INVALID_CREDENTIALS"],
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
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
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
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
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
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
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
            "code": RESPONSE_CODES["INVALID_CREDENTIALS"],
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
            "code": RESPONSE_CODES["INVALID_CREDENTIALS"],
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
            "code": RESPONSE_CODES["INVALID_CREDENTIALS"],
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
                "code": RESPONSE_CODES["INVALID_CREDENTIALS"],
                "data": None,
            }
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.json(), expected_response)

        # Now, even with correct credentials, the account should be locked
        data["password"] = self.password
        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["ACCOUNT_LOCKED"],
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
            "code": RESPONSE_CODES["INVALID_CREDENTIALS"],
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
            "code": RESPONSE_CODES["LOGOUT_SUCCESS"],
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
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)


class RegisterApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Seed initial data
        call_command("seed_groups")

        # Endpoint for registration
        cls.url = reverse("register")

        # User details for registration
        cls.username = "testuser"
        cls.password = "StrongPassword123"
        cls.email = "testuser@example.com"

        # Create an admin user
        cls.admin_user = UserModel.objects.create_user(
            username="admintest",
            password="12345678a",
            email="admintest@gmail.com",
            role=UserModel.Role.ADMIN,
        )

        # Create a regular (non-admin) user
        cls.regular_user = UserModel.objects.create_user(
            username="regulartest",
            password="password123",
            email="regular@example.com",
            role=UserModel.Role.USER,
        )

    def authenticate_as_admin(self):
        """Authenticate the test client as the admin user."""
        self.client.logout()
        self.client.login(username=self.admin_user.username, password="12345678a")

    def authenticate_as_regular_user(self):
        """Authenticate the test client as the regular user."""
        self.client.logout()
        self.client.login(username=self.regular_user.username, password="password123")

    def test_admin_can_register_user_successfully(self):
        """
        Ensure that an admin user can register a new user successfully.
        """
        self.authenticate_as_admin()

        data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": "USER",
        }

        response = self.client.post(self.url, data, format="json")

        user = UserModel.objects.get(username=self.username)
        user_data = UserSerializer(user).data

        expected_response = {
            "code": RESPONSE_CODES["REGISTRATION_SUCCESS"],
            "data": user_data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_regular_user_cannot_register_user(self):
        """
        Ensure that a non-admin user cannot register a new user.
        """
        self.authenticate_as_regular_user()

        data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_registration_with_existing_username(self):
        """
        Test that registration fails when the username already exists.
        """
        self.authenticate_as_admin()

        # Create a user with the same username
        UserModel.objects.create_user(
            username=self.username,
            password="DifferentPassword123",
            email="different@example.com",
        )

        data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],  # Validation errors
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_registration_with_invalid_email(self):
        """
        Test that registration fails with an invalid email format.
        """
        self.authenticate_as_admin()

        data = {
            "username": self.username,
            "password": self.password,
            "email": "invalid-email-format",
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_registration_with_missing_fields(self):
        """
        Test that registration fails when required fields are missing.
        """
        self.authenticate_as_admin()

        data = {
            "username": self.username,
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_registration_with_weak_password(self):
        """
        Test that registration fails when the password does not meet complexity requirements.
        """
        self.authenticate_as_admin()

        data = {
            "username": self.username,
            "password": "123",
            "email": self.email,
        }

        response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_registration_without_permission(self):
        """
        Test that registration fails when the user does not have admin permissions.
        """
        self.authenticate_as_regular_user()

        data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }

        with patch(
            "authentication.permissions.HasRegisterPermission.has_permission",
            return_value=False,
        ):
            response = self.client.post(self.url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)


class UserInfoApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-info")

        cls.username = "testuser"
        cls.password = "testpassword"
        cls.email = "testuser@example.com"
        cls.role = UserModel.Role.USER
        cls.user = UserModel.objects.create_user(
            username=cls.username,
            password=cls.password,
            email=cls.email,
            role=cls.role,
        )

    def test_get_user_info_authenticated(self):
        """
        Test that an authenticated user can retrieve their own information.
        """
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.url)

        expected_response = {
            "code": RESPONSE_CODES["USER_INFO_SUCCESS"],
            "data": {
                "username": self.username,
                "email": self.email,
                "role": self.role,
            },
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_get_user_info_unauthenticated(self):
        """
        Test that an unauthenticated user receives a 403 Forbidden response.
        """
        response = self.client.get(self.url)

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)