"""
Phone authentication serializers
"""
from typing import Any
from rest_framework import serializers


class PhoneAuthRequestSerializer(serializers.Serializer[Any]):
    """
    Phone authentication request
    Similar to functions/auth.py PhoneAuthRequest
    """
    phone = serializers.CharField(min_length=11, max_length=16)
    first_name = serializers.CharField(min_length=1, max_length=100)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    username = serializers.CharField(min_length=3, max_length=32, required=False, allow_blank=True)

    def validate_phone(self, value: str) -> str:
        """Validate phone number format"""
        cleaned = ''.join(c for c in value if c.isdigit() or c == '+')
        
        if not cleaned.startswith('+'):
            raise serializers.ValidationError("Phone number must start with +")
        
        digits = cleaned[1:]
        if len(digits) < 10 or len(digits) > 15:
            raise serializers.ValidationError("Phone number must contain 10-15 digits")
        
        return cleaned
