"""
Common validators
"""
import re
from rest_framework import serializers


def validate_password_strength(password: str) -> str:
    """
    Validate password strength
    
    Requirements:
    - At least 8 characters
    - At least one digit
    - At least one uppercase letter
    - At least one lowercase letter
    
    Args:
        password: Password string
        
    Returns:
        Validated password
        
    Raises:
        serializers.ValidationError: If password doesn't meet requirements
    """
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters")
    
    if not any(c.isdigit() for c in password):
        raise serializers.ValidationError("Password must contain at least one digit")
    
    if not any(c.isupper() for c in password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        raise serializers.ValidationError("Password must contain at least one lowercase letter")
    
    return password


def validate_phone_number(phone: str) -> str:
    """
    Validate phone number format
    
    Requirements:
    - Must start with +
    - 10-15 digits after +
    
    Args:
        phone: Phone number string
        
    Returns:
        Cleaned phone number
        
    Raises:
        serializers.ValidationError: If phone format is invalid
    """
    cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
    
    if not cleaned.startswith('+'):
        raise serializers.ValidationError("Phone number must start with +")
    
    digits = cleaned[1:]
    if len(digits) < 10 or len(digits) > 15:
        raise serializers.ValidationError("Phone number must contain 10-15 digits")
    
    return cleaned


def validate_username(username: str) -> str:
    """
    Validate username format
    
    Requirements:
    - 3-32 characters
    - Only alphanumeric characters and underscore
    
    Args:
        username: Username string
        
    Returns:
        Validated username
        
    Raises:
        serializers.ValidationError: If username format is invalid
    """
    if len(username) < 3:
        raise serializers.ValidationError("Username must be at least 3 characters")
    
    if len(username) > 32:
        raise serializers.ValidationError("Username must not exceed 32 characters")
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise serializers.ValidationError("Username can only contain letters, numbers, and underscore")
    
    return username
