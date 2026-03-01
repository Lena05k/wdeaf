"""
API Serializers
"""
from .auth import (
    EmailLoginRequestSerializer,
    EmailSignupRequestSerializer,
    RefreshTokenRequestSerializer,
    AuthResponseSerializer,
)
from .user import UserSerializer, UserUpdateSerializer
from .provider import ProviderSignupRequestSerializer, ProviderListSerializer
from .telegram import TelegramAuthRequestSerializer
from .phone import PhoneAuthRequestSerializer

__all__ = [
    # Auth
    'EmailLoginRequestSerializer',
    'EmailSignupRequestSerializer',
    'RefreshTokenRequestSerializer',
    'AuthResponseSerializer',
    # User
    'UserSerializer',
    'UserUpdateSerializer',
    # Provider
    'ProviderSignupRequestSerializer',
    'ProviderListSerializer',
    # Telegram
    'TelegramAuthRequestSerializer',
    # Phone
    'PhoneAuthRequestSerializer',
]
