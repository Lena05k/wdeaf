"""
JWT utilities for authentication
"""
from typing import Any, Optional
from datetime import datetime, timedelta
import jwt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def _get_jwt_secret() -> str:
    """Get JWT secret key from settings"""
    jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
    return jwt_settings.get('SIGNING_KEY', settings.SECRET_KEY)


def _get_jwt_algorithm() -> str:
    """Get JWT algorithm from settings"""
    jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
    return jwt_settings.get('ALGORITHM', 'HS256')


def create_access_token(user_id: int, expires_hours: Optional[int] = None) -> str:
    """Create JWT access token"""
    jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
    exp = expires_hours or int(jwt_settings.get('ACCESS_TOKEN_LIFETIME', timedelta(hours=24)).total_seconds() / 3600)
    payload = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=exp),
        'iat': datetime.utcnow(),
        'token_type': 'access',
        'jti': f'{user_id}-{datetime.utcnow().isoformat()}',  # Unique token ID
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=_get_jwt_algorithm())


def create_refresh_token(user_id: int) -> str:
    """Create JWT refresh token"""
    jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
    exp = int(jwt_settings.get('REFRESH_TOKEN_LIFETIME', timedelta(days=30)).total_seconds() / 86400)
    payload = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=exp),
        'iat': datetime.utcnow(),
        'token_type': 'refresh',
        'jti': f'{user_id}-refresh-{datetime.utcnow().isoformat()}',  # Unique token ID
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=_get_jwt_algorithm())


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT token"""
    try:
        return jwt.decode(token, _get_jwt_secret(), algorithms=[_get_jwt_algorithm()])
    except jwt.InvalidTokenError as e:
        logger.error(f"❌ Token decode error: {e}")
        raise
