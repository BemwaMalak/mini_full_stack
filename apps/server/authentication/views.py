from django.contrib.auth import authenticate, get_user_model, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.views import APIView

from app.response_codes import RESPONSE_CODES
from app.utils import json_response, ratelimit

from .permissions import HasRegisterPermission
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer

UserModel = get_user_model()


class LoginApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    @method_decorator(csrf_protect)
    @method_decorator(ratelimit(key="ip", rate="5/30s", method="POST", block=True))
    def post(self, request):
        # Check if the request was blocked by the rate limit
        if getattr(request, "limited", False):
            return json_response(
                code=RESPONSE_CODES["TOO_MANY_REQUESTS"],
                data=None,
                status_code=HTTP_403_FORBIDDEN,
            )

        # Validate login data
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            # Retrieve the user by username
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                user = None

            if user:
                # Check if the account is locked due to multiple failed login attempts
                if user.is_locked:
                    return json_response(
                        code=RESPONSE_CODES["ACCOUNT_LOCKED"],
                        data=None,
                        status_code=HTTP_403_FORBIDDEN,
                    )

                # Authenticate the user
                user_auth = authenticate(
                    request=request, username=username, password=password
                )
                if user_auth:
                    # Successful login: reset failed login attempts
                    user.failed_login_attempts = 0
                    user.save()

                    login(request, user_auth)
                    user_data = UserSerializer(user_auth).data
                    return json_response(
                        code=RESPONSE_CODES["LOGIN_SUCCESS"],
                        data=user_data,
                        status_code=HTTP_200_OK,
                    )
                else:
                    # Failed authentication: increment failed login attempts
                    user.failed_login_attempts += 1
                    if user.failed_login_attempts >= 5:
                        user.is_locked = True
                    user.save()
                    return json_response(
                        code=RESPONSE_CODES["INVALID_CREDENTIALS"],
                        data=None,
                        status_code=HTTP_401_UNAUTHORIZED,
                    )
            else:
                # User not found
                return json_response(
                    code=RESPONSE_CODES["INVALID_CREDENTIALS"],
                    data=None,
                    status_code=HTTP_401_UNAUTHORIZED,
                )

        # Validation failed
        return json_response(
            code=RESPONSE_CODES["VALIDATION_ERROR"],
            data=serializer.errors,
            status_code=HTTP_400_BAD_REQUEST,
        )


class LogoutApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return json_response(
            code=RESPONSE_CODES["LOGOUT_SUCCESS"],
            data=None,
            status_code=HTTP_200_OK,
        )


class RegisterApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [HasRegisterPermission]

    @method_decorator(csrf_protect)
    @method_decorator(ratelimit(key="ip", rate="5/30s", method="POST", block=True))
    def post(self, request):
        # Check if the request was blocked by the rate limit
        if getattr(request, "limited", False):
            return json_response(
                code=RESPONSE_CODES["TOO_MANY_REQUESTS"],
                data=None,
                status_code=HTTP_403_FORBIDDEN,
            )

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return json_response(
                code=RESPONSE_CODES["REGISTRATION_SUCCESS"],
                data=user_data,
                status_code=HTTP_200_OK,
            )

        # Validation failed
        return json_response(
            code=RESPONSE_CODES["VALIDATION_ERROR"],
            data=serializer.errors,
            status_code=HTTP_400_BAD_REQUEST,
        )

class UserInfoApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "role": request.user.role,
        }
        return json_response(
            code=RESPONSE_CODES["USER_INFO_SUCCESS"],
            data=user_data,
            status_code=HTTP_200_OK,
        )
 