from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView

from app.response_codes import RESPONSE_CODES
from app.utils import json_response, ratelimit

from .models import Medication, RefillRequest
from .permissions import HasMedicationPermission, HasRefillRequestPermission
from .serializers import MedicationSerializer, RefillRequestDetailSerializer, RefillRequestSerializer


class MedicationApiView(APIView):
    permission_classes = [IsAuthenticated, HasMedicationPermission]

    @method_decorator(ratelimit(key="ip", rate="10/m", method="GET", block=True))
    def get(self, request, pk=None):
        if getattr(request, "limited", False):
            return json_response(
                code=RESPONSE_CODES["TOO_MANY_REQUESTS"],
                data=None,
                status_code=HTTP_400_BAD_REQUEST,
            )

        if pk:
            try:
                medication = Medication.objects.get(pk=pk)
            except Medication.DoesNotExist:
                return json_response(
                    code=RESPONSE_CODES["MEDICATION_NOT_FOUND"],
                    data=None,
                    status_code=HTTP_404_NOT_FOUND,
                )
            serializer = MedicationSerializer(medication, context={"request": request})
            return json_response(
                code=RESPONSE_CODES["MEDICATION_DETAIL_SUCCESS"],
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        else:
            medications = Medication.objects.all()
            serializer = MedicationSerializer(
                medications, many=True, context={"request": request}
            )
            return json_response(
                code=RESPONSE_CODES["MEDICATION_LIST_SUCCESS"],
                data=serializer.data,
                status_code=HTTP_200_OK,
            )

    @method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True))
    def post(self, request):
        if getattr(request, "limited", False):
            return json_response(
                code=RESPONSE_CODES["TOO_MANY_REQUESTS"],
                data=None,
                status_code=HTTP_400_BAD_REQUEST,
            )

        serializer = MedicationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            return json_response(
                code=RESPONSE_CODES["MEDICATION_CREATED"],
                data=serializer.data,
                status_code=HTTP_201_CREATED,
            )
        return json_response(
            code=RESPONSE_CODES["VALIDATION_ERROR"],
            data=serializer.errors,
            status_code=HTTP_400_BAD_REQUEST,
        )

    @method_decorator(ratelimit(key="ip", rate="5/m", method="PUT", block=True))
    def put(self, request, pk=None):
        """
        Update an existing medication's details.
        """
        if pk is None:
            return json_response(
                code=RESPONSE_CODES["VALIDATION_ERROR"],
                data="Medication ID is required",
                status_code=HTTP_400_BAD_REQUEST,
            )

        try:
            medication = Medication.objects.get(pk=pk)
        except Medication.DoesNotExist:
            return json_response(
                code=RESPONSE_CODES["MEDICATION_NOT_FOUND"],
                data=None,
                status_code=HTTP_404_NOT_FOUND,
            )

        serializer = MedicationSerializer(
            medication, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return json_response(
                code=RESPONSE_CODES["MEDICATION_UPDATED"],
                data=serializer.data,
                status_code=HTTP_200_OK,
            )

        return json_response(
            code=RESPONSE_CODES["VALIDATION_ERROR"],
            data=serializer.errors,
            status_code=HTTP_400_BAD_REQUEST,
        )

    @method_decorator(ratelimit(key="ip", rate="5/m", method="DELETE", block=True))
    def delete(self, request, pk=None):
        """
        Delete an existing medication.
        """
        if pk is None:
            return json_response(
                code=RESPONSE_CODES["VALIDATION_ERROR"],
                data="Medication ID is required",
                status_code=HTTP_400_BAD_REQUEST,
            )

        try:
            medication = Medication.objects.get(pk=pk)
        except Medication.DoesNotExist:
            return json_response(
                code=RESPONSE_CODES["MEDICATION_NOT_FOUND"],
                data=None,
                status_code=HTTP_404_NOT_FOUND,
            )

        medication.delete()
        return json_response(
            code=RESPONSE_CODES["MEDICATION_DELETED"],
            data=None,
            status_code=HTTP_200_OK,
        )


class RefillRequestApiView(APIView):
    permission_classes = [IsAuthenticated, HasRefillRequestPermission]

    @method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True))
    def post(self, request):
        if getattr(request, "limited", False):
            return json_response(
                code=RESPONSE_CODES["TOO_MANY_REQUESTS"],
                data=None,
                status_code=HTTP_400_BAD_REQUEST,
            )

        serializer = RefillRequestSerializer(data=request.data)
        if serializer.is_valid():
            medication_id = request.data.get("medication")
            try:
                medication = Medication.objects.get(id=medication_id)
            except Medication.DoesNotExist:
                return json_response(
                    code=RESPONSE_CODES["REFILL_REQUEST_NOT_FOUND"],
                    data=None,
                    status_code=HTTP_404_NOT_FOUND,
                )

            refill_request = serializer.save(user=request.user, medication=medication)
            return json_response(
                code=RESPONSE_CODES["REFILL_REQUEST_CREATED"],
                data=RefillRequestSerializer(refill_request).data,
                status_code=HTTP_201_CREATED,
            )

        return json_response(
            code=RESPONSE_CODES["VALIDATION_ERROR"],
            data=serializer.errors,
            status_code=HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        """
        List refill requests for the authenticated user.
        """
        refill_requests = None
        if request.user.role == "ADMIN":
            refill_requests = RefillRequest.objects.all()
        else:
            refill_requests = RefillRequest.objects.filter(user=request.user)
        serializer = RefillRequestDetailSerializer(refill_requests, many=True)
        return json_response(
            code=RESPONSE_CODES["REFILL_REQUEST_LIST_SUCCESS"],
            data=serializer.data,
            status_code=HTTP_200_OK,
        )

    def put(self, request, pk=None):
        """
        Update the status of a specific refill request.
        """
        if pk is None:
            return json_response(
                code=RESPONSE_CODES["VALIDATION_ERROR"],
                data="Request ID is required",
                status_code=HTTP_400_BAD_REQUEST,
            )

        try:
            refill_request = RefillRequest.objects.get(pk=pk)
        except RefillRequest.DoesNotExist:
            return json_response(
                code=RESPONSE_CODES["REFILL_REQUEST_NOT_FOUND"],
                data=None,
                status_code=HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")
        if new_status not in dict(RefillRequest.STATUS_CHOICES):
            return json_response(
                code=RESPONSE_CODES["VALIDATION_ERROR"],
                data="Invalid status",
                status_code=HTTP_400_BAD_REQUEST,
            )

        refill_request.status = new_status
        refill_request.save()
        return json_response(
            code=RESPONSE_CODES["REFILL_REQUEST_UPDATED"],
            data=RefillRequestSerializer(refill_request).data,
            status_code=HTTP_200_OK,
        )
