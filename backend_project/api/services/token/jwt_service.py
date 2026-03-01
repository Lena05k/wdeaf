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
        """Получить секретный ключ JWT"""
        return self._secret
    
    def _get_algorithm(self) -> str:
        """Получить алгоритм JWT"""
        return self._algorithm
    
    def create_access_token(self, user_id: int, expires_hours: Optional[int] = None) -> str:
        """
        Создать JWT access токен
        
        Args:
            user_id: ID пользователя
            expires_hours: Время жизни токена в часах
            
        Returns:
            Строка JWT токена
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
        Создать JWT refresh токен
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Строка JWT токена
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
        Декодировать и проверить JWT токен
        
        Args:
            token: Строка JWT токена
            
        Returns:
            Расшифрованный payload токена
            
        Raises:
            jwt.InvalidTokenError: Если токен невалиден или истёк
        """
        return jwt.decode(token, self._get_secret(), algorithms=[self._get_algorithm()])
    
    def validate_token(self, token: str) -> bool:
        """
        Проверить JWT токен без декодирования
        
        Args:
            token: Строка JWT токена
            
        Returns:
            True если токен валиден
        """
        try:
            self.decode_token(token)
            return True
        except jwt.InvalidTokenError:
            return False
