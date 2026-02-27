from typing import Any
from rest_framework import serializers
from .models import User
import hashlib
import hmac
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            'id', 'telegram_id', 'email', 'phone',
            'first_name', 'last_name', 'username',
            'avatar_url', 'is_provider', 'auth_provider'
        ]
        read_only_fields = ['id']


class AuthResponseSerializer(serializers.Serializer[Any]):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField(default='bearer')
    user = UserSerializer()


class EmailLoginRequestSerializer(serializers.Serializer[Any]):
    email = serializers.EmailField(min_length=5, max_length=255)
    password = serializers.CharField(min_length=8, max_length=128)


class EmailSignupRequestSerializer(serializers.Serializer[Any]):
    email = serializers.EmailField(min_length=5, max_length=255)
    password = serializers.CharField(min_length=8, max_length=128)
    first_name = serializers.CharField(min_length=1, max_length=100)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_password(self, value: str) -> str:
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Password must contain at least one digit")
        return value


class PhoneAuthRequestSerializer(serializers.Serializer[Any]):
    phone = serializers.CharField(max_length=15, min_length=10)
    first_name = serializers.CharField(min_length=1, max_length=100)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    username = serializers.CharField(max_length=32, min_length=3, required=False, allow_blank=True)

    def validate_phone(self, value: str) -> str:
        if not value.startswith("+"):
            raise serializers.ValidationError("Phone must start with +")
        return value


class RefreshTokenRequestSerializer(serializers.Serializer[Any]):
    refresh_token = serializers.CharField()