from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.response_codes import RESPONSE_CODES
from medication.models import Medication, RefillRequest
from medication.serializers import MedicationSerializer, RefillRequestSerializer

UserModel = get_user_model()


class MedicationApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse("medication-list-create")
        # Assuming "medication-detail-update" is the name for detail routes
        cls.detail_url_template = "medication-detail-update"

        # Admin user who can add, update, and delete medications
        cls.admin_user = UserModel.objects.create_user(
            username="adminuser",
            password="adminpass",
            email="admin@example.com",
            role=UserModel.Role.ADMIN,
        )

        # Regular user who cannot add, update, or delete medications
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

    # Existing Tests
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

        response = self.client.post(self.list_url, data, format="json")

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

        response = self.client.post(self.list_url, data, format="json")

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

        response = self.client.post(self.list_url, data, format="json")

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

    # New Tests for Update
    def test_update_medication_with_admin_permission(self):
        """
        Test updating a medication with an admin user
        """
        self.client.login(username=self.admin_user.username, password="adminpass")

        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})
        data = {
            "dosage": "20mg",
            "quantity": 30,
        }

        response = self.client.put(detail_url, data, format="json")
        medication.refresh_from_db()
        serializer = MedicationSerializer(medication)

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_UPDATED"],
            "data": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_update_medication_without_admin_permission(self):
        """
        Test that a regular user cannot update a medication
        """
        self.client.login(username=self.regular_user.username, password="userpass")

        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})
        data = {
            "dosage": "20mg",
            "quantity": 30,
        }

        response = self.client.put(detail_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_update_nonexistent_medication(self):
        """
        Test updating a medication that does not exist
        """
        self.client.login(username=self.admin_user.username, password="adminpass")

        detail_url = reverse("medication-detail-update", kwargs={"pk": 9999})
        data = {
            "dosage": "20mg",
            "quantity": 30,
        }

        response = self.client.put(detail_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_NOT_FOUND"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), expected_response)

    def test_delete_medication_with_admin_permission(self):
        """
        Test deleting a medication with an admin user
        """
        self.client.login(username=self.admin_user.username, password="adminpass")

        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})

        response = self.client.delete(detail_url)

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_DELETED"],
            "data": None,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)
        self.assertFalse(Medication.objects.filter(pk=medication.pk).exists())

    def test_delete_medication_without_admin_permission(self):
        """
        Test that a regular user cannot delete a medication
        """
        self.client.login(username=self.regular_user.username, password="userpass")

        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})

        response = self.client.delete(detail_url)

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)
        self.assertTrue(Medication.objects.filter(pk=medication.pk).exists())

    def test_delete_nonexistent_medication(self):
        """
        Test deleting a medication that does not exist
        """
        self.client.login(username=self.admin_user.username, password="adminpass")

        detail_url = reverse("medication-detail-update", kwargs={"pk": 9999})

        response = self.client.delete(detail_url)

        expected_response = {
            "code": RESPONSE_CODES["MEDICATION_NOT_FOUND"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_list_medications(self):
        """
        Test that unauthenticated users cannot access the medication list
        """
        response = self.client.get(self.list_url)

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_retrieve_medication(self):
        """
        Test that unauthenticated users cannot retrieve medication details
        """
        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})

        response = self.client.get(detail_url)

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_create_medication(self):
        """
        Test that unauthenticated users cannot create a medication
        """
        data = {
            "name": "New Medication",
            "dosage": "10mg",
            "quantity": 20,
            "instructions": "Take once daily",
        }

        response = self.client.post(self.list_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_update_medication(self):
        """
        Test that unauthenticated users cannot update a medication
        """
        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})
        data = {
            "dosage": "20mg",
            "quantity": 30,
        }

        response = self.client.put(detail_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_delete_medication(self):
        """
        Test that unauthenticated users cannot delete a medication
        """
        medication = Medication.objects.first()
        detail_url = reverse("medication-detail-update", kwargs={"pk": medication.pk})

        response = self.client.delete(detail_url)

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)


from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.response_codes import RESPONSE_CODES

from .models import Medication, RefillRequest, UserModel
from .serializers import RefillRequestSerializer


class RefillRequestApiViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse("refillrequest-list-create")
        cls.detail_url_template = "refillrequest-detail-update"

        cls.admin_user = UserModel.objects.create_user(
            username="adminuser",
            password="adminpass",
            email="admin@example.com",
            role=UserModel.Role.ADMIN,
        )

        cls.regular_user = UserModel.objects.create_user(
            username="testuser",
            password="userpass",
            email="test@example.com",
            role=UserModel.Role.USER,
        )

        cls.medication = Medication.objects.create(
            name="Test Medication",
            dosage="10mg",
            quantity=50,
            instructions="Take twice daily",
            added_by=cls.admin_user,
        )

        call_command("seed_groups")

    def setUp(self):
        self.client.logout()

    def test_create_refill_request_as_authenticated_user(self):
        self.client.login(username=self.regular_user.username, password="userpass")
        data = {
            "medication": self.medication.id,
            "quantity": 5,
        }

        response = self.client.post(self.list_url, data, format="json")
        refill_request = RefillRequest.objects.get(
            user=self.regular_user, medication=self.medication
        )
        serializer = RefillRequestSerializer(refill_request)

        expected_response = {
            "code": RESPONSE_CODES["REFILL_REQUEST_CREATED"],
            "data": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_response)

    def test_create_refill_request_as_unauthenticated_user(self):
        data = {
            "medication": self.medication.id,
            "quantity": 5,
        }

        response = self.client.post(self.list_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_create_refill_request_for_nonexistent_medication(self):
        self.client.login(username=self.regular_user.username, password="userpass")
        data = {
            "medication": 9999,
            "quantity": 5,
        }

        response = self.client.post(self.list_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
            "data": {"medication": ['Invalid pk "9999" - object does not exist.']},
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_create_refill_request_with_invalid_data(self):
        self.client.login(username=self.regular_user.username, password="userpass")
        data = {}

        response = self.client.post(self.list_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["VALIDATION_ERROR"],
            "data": response.data["data"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)

    def test_list_refill_requests_as_authenticated_user(self):
        RefillRequest.objects.create(
            user=self.regular_user, medication=self.medication, status="PENDING"
        )
        RefillRequest.objects.create(
            user=self.regular_user, medication=self.medication, status="APPROVED"
        )

        self.client.login(username=self.regular_user.username, password="userpass")

        response = self.client.get(self.list_url)
        refill_requests = RefillRequest.objects.filter(user=self.regular_user)
        serializer = RefillRequestSerializer(refill_requests, many=True)

        expected_response = {
            "code": RESPONSE_CODES["REFILL_REQUEST_LIST_SUCCESS"],
            "data": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_list_refill_requests_as_unauthenticated_user(self):
        response = self.client.get(self.list_url)

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_update_refill_request_status_as_owner(self):
        refill_request = RefillRequest.objects.create(
            user=self.regular_user, medication=self.medication, status="PENDING"
        )
        detail_url = reverse(
            "refillrequest-detail-update", kwargs={"pk": refill_request.pk}
        )

        self.client.login(username=self.admin_user.username, password="adminpass")
        data = {
            "status": "APPROVED",
        }

        response = self.client.put(detail_url, data, format="json")
        refill_request.refresh_from_db()
        serializer = RefillRequestSerializer(refill_request)

        expected_response = {
            "code": RESPONSE_CODES["REFILL_REQUEST_UPDATED"],
            "data": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(refill_request.status, "APPROVED")

    def test_update_refill_request_status_as_non_owner(self):
        other_user = UserModel.objects.create_user(
            username="otheruser",
            password="otherpass",
            email="other@example.com",
            role=UserModel.Role.USER,
        )
        refill_request = RefillRequest.objects.create(
            user=other_user, medication=self.medication, status="PENDING"
        )
        detail_url = reverse(
            "refillrequest-detail-update", kwargs={"pk": refill_request.pk}
        )

        self.client.login(username=self.regular_user.username, password="userpass")
        data = {
            "status": "APPROVED",
        }

        response = self.client.put(detail_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)
        refill_request.refresh_from_db()
        self.assertEqual(refill_request.status, "PENDING")

    def test_update_nonexistent_refill_request(self):
        self.client.login(username=self.admin_user.username, password="adminpass")
        detail_url = reverse("refillrequest-detail-update", kwargs={"pk": 9999})
        data = {
            "status": "APPROVED",
        }

        response = self.client.put(detail_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["REFILL_REQUEST_NOT_FOUND"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_create_refill_request(self):
        data = {
            "medication": self.medication.id,
            "quantity": 5,
        }

        response = self.client.post(self.list_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_list_refill_requests(self):
        response = self.client.get(self.list_url)

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)

    def test_unauthenticated_access_update_refill_request(self):
        refill_request = RefillRequest.objects.create(
            user=self.regular_user, medication=self.medication, status="PENDING"
        )
        detail_url = reverse(
            "refillrequest-detail-update", kwargs={"pk": refill_request.pk}
        )
        data = {
            "status": "APPROVED",
        }

        response = self.client.put(detail_url, data, format="json")

        expected_response = {
            "code": RESPONSE_CODES["FORBIDDEN"],
            "data": None,
        }

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected_response)
