from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.response_codes import RESPONSE_CODES
from medication.models import Medication
from medication.serializers import MedicationSerializer

UserModel = get_user_model()

class MedicationApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse("medication-list-create")
        cls.create_url = cls.list_url
        cls.detail_url_template = "medication/<int:pk>/"

        # Admin user who can add medications
        cls.admin_user = UserModel.objects.create_user(
            username="adminuser",
            password="adminpass",
            email="admin@example.com",
            role=UserModel.Role.ADMIN,
        )

        # Regular user who cannot add medications
        cls.regular_user = UserModel.objects.create_user(
            username="testuser",
            password="userpass",
            email="test@example.com",
            role=UserModel.Role.USER,
        )        

        call_command("seed_medications")
        call_command("seed_groups")

    def setUp(self):
        # Ensure users are logged out before each test
        self.client.logout()

    def test_list_medications(self):
        """
        Test listing all medications
        """
        self.client.login(username=self.regular_user.username, password="userpass")

        response = self.client.get(self.list_url)
        medications = Medication.objects.all()
        serializer = MedicationSerializer(medications, many=True)

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_LIST_SUCCESS"],
            "data": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_retrieve_medication_detail(self):
        """
        Test retrieving details of a specific medication
        """
        self.client.login(username=self.regular_user.username, password="userpass")

        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})

        response = self.client.get(detail_url)
        serializer = MedicationSerializer(medication)

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_DETAIL_SUCCESS"],
            "data": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_create_medication_with_admin_permission(self):
        """
        Test creating a medication with an admin user
        """
        self.client.login(username=self.admin_user.username, password="adminpass")
        data = {
            "name": "New Medication",
            "dosage": "10mg",
            "quantity": 20,
            "instructions": "Take once daily",
        }

        response = self.client.post(self.create_url, data, format="json")

        medication = Medication.objects.get(name="New Medication")
        serializer = MedicationSerializer(medication)

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_CREATED"],
            "data": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_response)

    def test_create_medication_without_admin_permission(self):
        """
        Test that a regular user cannot create a medication
        """
        self.client.login(username=self.regular_user.username, password="userpass")
        data = {
            "name": "Unauthorized Medication",
            "dosage": "10mg",
            "quantity": 20,
            "instructions": "Take once daily",
        }

        response = self.client.post(self.create_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_create_medication_with_missing_fields(self):
        """
        Test creating a medication with missing required fields
        """
        self.client.login(username=self.admin_user.username, password="adminpass")
        data = {
            "name": "Incomplete Medication",
        }

        response = self.client.post(self.create_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_retrieve_nonexistent_medication(self):
        """
        Test retrieving a medication that does not exist
        """
        self.client.login(username=self.regular_user.username, password="userpass")
        
        detail_url = reverse("medication-detail-update", kwargs={"pk": 9999})

        response = self.client.get(detail_url)

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_NOT_FOUND"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), expected_response)
