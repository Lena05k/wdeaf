"""
JWT token service
Handles JWT token creation and validation
"""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import jwt
from django.conf import settings


class JWTService:
    """Service for JWT token operations"""
    
    def __init__(self):
        self._jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        self._secret = self._jwt_settings.get('SIGNING_KEY', settings.SECRET_KEY)
        self._algorithm = self._jwt_settings.get('ALGORITHM', 'HS256')
    
    def _get_secret(self) -> str:
        """Get JWT secret key"""
        return self._secret
    
    def _get_algorithm(self) -> str:
        """Get JWT algorithm"""
        return self._algorithm
    
    def create_access_token(self, user_id: int, expires_hours: Optional[int] = None) -> str:
        """
        Create JWT access token
        
        Args:
            user_id: User ID
            expires_hours: Token expiration in hours
            
        Returns:
            JWT token string
        """
        exp = expires_hours or int(
            self._jwt_settings.get('ACCESS_TOKEN_LIFETIME', timedelta(hours=24)).total_seconds() / 3600
        )
        
        payload = {
            'sub': str(user_id),
            'exp': datetime.utcnow() + timedelta(hours=exp),
            'iat': datetime.utcnow(),
            'token_type': 'access',
            'jti': f'{user_id}-{datetime.utcnow().isoformat()}',
        }
        
        return jwt.encode(payload, self._get_secret(), algorithm=self._get_algorithm())
    
    def create_refresh_token(self, user_id: int) -> str:
        """
        Create JWT refresh token
        
        Args:
            user_id: User ID
            
        Returns:
            JWT token string
        """
        exp = int(
            self._jwt_settings.get('REFRESH_TOKEN_LIFETIME', timedelta(days=30)).total_seconds() / 86400
        )
        
        payload = {
            'sub': str(user_id),
            'exp': datetime.utcnow() + timedelta(days=exp),
            'iat': datetime.utcnow(),
            'token_type': 'refresh',
            'jti': f'{user_id}-refresh-{datetime.utcnow().isoformat()}',
        }
        
        return jwt.encode(payload, self._get_secret(), algorithm=self._get_algorithm())
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
        """
        return jwt.decode(token, self._get_secret(), algorithms=[self._get_algorithm()])
    
    def validate_token(self, token: str) -> bool:
        """
        Validate JWT token without decoding
        
        Args:
            token: JWT token string
            
        Returns:
            True if token is valid
        """
        try:
            self.decode_token(token)
            return True
        except jwt.InvalidTokenError:
            return False
