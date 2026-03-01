"""
Auth services
"""
from .email_auth import EmailAuthService
from .telegram_auth import TelegramAuthService
from .phone_auth import PhoneAuthService
from .provider_auth import ProviderAuthService

__all__ = [
    'EmailAuthService',
    'TelegramAuthService',
    'PhoneAuthService',
    'ProviderAuthService',
]
