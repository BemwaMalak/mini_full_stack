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

from .models import Medication
from .permissions import HasMedicationPermission
from .serializers import MedicationSerializer


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
            serializer = MedicationSerializer(medication)
            return json_response(
                code=RESPONSE_CODES["MEDICATION_DETAIL_SUCCESS"],
                data=serializer.data,
                status_code=HTTP_200_OK,
            )
        else:
            medications = Medication.objects.all()
            serializer = MedicationSerializer(medications, many=True)
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

        serializer = MedicationSerializer(data=request.data)
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
