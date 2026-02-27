"""
API Tests
"""
from .test_auth import AuthTestCase
from .test_user_profile import UserprofileTestCase
from .test_provider import ProviderTestCase

__all__ = [
    'AuthTestCase',
    'UserprofileTestCase',
    'ProviderTestCase',
]
