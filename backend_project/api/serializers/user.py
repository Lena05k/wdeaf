"""
User serializers
"""
from typing import Any
from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            'id', 'telegram_id', 'email', 'phone',
            'first_name', 'last_name', 'username',
            'avatar_url', 'is_provider', 'auth_provider'
        ]
        read_only_fields = ['id']


class UserUpdateSerializer(serializers.ModelSerializer[User]):
    """
    User profile update serializer
    Allows partial or full update of user profile
    """
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'avatar_url',
        ]
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'username': {'required': False, 'allow_blank': True},
            'avatar_url': {'required': False, 'allow_blank': True},
        }

    def validate_username(self, value: str) -> str:
        """Validate username format"""
        if value and len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters")
        if value and len(value) > 32:
            raise serializers.ValidationError("Username must not exceed 32 characters")
        return value
