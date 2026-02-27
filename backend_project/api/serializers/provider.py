"""
Provider serializers
"""
from typing import Any
from rest_framework import serializers
from api.models import User


class ProviderSignupRequestSerializer(serializers.Serializer[Any]):
    """
    Provider registration request
    Similar to email signup but sets is_provider=True
    """
    email = serializers.EmailField(min_length=5, max_length=255)
    password = serializers.CharField(min_length=8, max_length=128)
    first_name = serializers.CharField(min_length=1, max_length=100)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    company_name = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_password(self, value: str) -> str:
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Password must contain at least one digit")
        return value


class ProviderListSerializer(serializers.ModelSerializer[User]):
    """
    Provider list item serializer
    Shows public provider information
    """
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone',
            'email',
            'created_at',
        ]
        read_only_fields = fields
