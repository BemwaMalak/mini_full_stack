from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.server.authentication.serializers import LoginSerializer, UserSerializer
from app.utils import json_response
from .enums import Message


class LoginApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    @method_decorator(csrf_protect)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request=request, username=username, password=password)
            if user:
                login(request, user)
                user_data = UserSerializer(user).data
                return json_response(
                    message=Message.LOGIN_SUCCESS.value,
                    data=user_data,
                    status_code=HTTP_200_OK,
                )
            else:
                return json_response(
                    message=Message.INVALID_CREDENTIALS.value,
                    data=None,
                    status_code=HTTP_401_UNAUTHORIZED,
                )

        return json_response(
            message=Message.VALIDATION_ERROR.value,
            data=serializer.errors,
            status_code=HTTP_400_BAD_REQUEST,
        )
