from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, style={"input_type": "password"}, write_only=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "role"]
