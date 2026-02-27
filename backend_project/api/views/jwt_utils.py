"""
JWT utilities for authentication
"""
from typing import Any, Optional
from datetime import datetime, timedelta
import jwt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def create_access_token(user_id: int, expires_hours: Optional[int] = None) -> str:
    """Create JWT access token"""
    exp = expires_hours or getattr(settings, 'JWT_EXPIRATION_HOURS', 24)
    payload = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=exp),
        'iat': datetime.utcnow(),
        'type': 'access',
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=getattr(settings, 'JWT_ALGORITHM', 'HS256'))


def create_refresh_token(user_id: int) -> str:
    """Create JWT refresh token"""
    payload = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow(),
        'type': 'refresh',
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=getattr(settings, 'JWT_ALGORITHM', 'HS256'))


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT token"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[getattr(settings, 'JWT_ALGORITHM', 'HS256')])
    except jwt.InvalidTokenError as e:
        logger.error(f"❌ Token decode error: {e}")
        raise
