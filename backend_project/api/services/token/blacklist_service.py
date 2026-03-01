"""
Token blacklist service
Handles Redis-based token blacklisting for logout
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple
import redis
from django.conf import settings

logger = logging.getLogger(__name__)


def get_redis_client() -> Optional[redis.Redis]:
    """Получить Redis клиент из настроек"""
    redis_config = getattr(settings, 'REDIS', {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None
    })
    
    try:
        client = redis.Redis(
            host=redis_config.get('host', 'localhost'),
            port=redis_config.get('port', 6379),
            db=redis_config.get('db', 0),
            password=redis_config.get('password'),
            decode_responses=True
        )
        client.ping()
        return client
    except redis.ConnectionError as e:
        logger.warning(f"Redis connection failed: {e}")
        return None


class TokenBlacklistService:
    """Сервис для операций с blacklist токенов"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
    
    def add_to_blacklist(self, token: str, expires_at: datetime) -> Tuple[Optional[str], bool]:
        """
        Добавить токен в blacklist
        
        Args:
            token: Строка JWT токена
            expires_at: Время истечения токена
            
        Returns:
            Кортеж (сообщение_об_ошибке, успех)
        """
        if self.redis_client is None:
            logger.warning("Redis недоступен, токен не будет добавлен в blacklist")
            return None, True
        
        try:
            ttl = int((expires_at - datetime.utcnow()).total_seconds())
            if ttl <= 0:
                ttl = 3600
            
            blacklist_key = f"token_blacklist:{token}"
            self.redis_client.setex(blacklist_key, ttl, "blacklisted")
            
            logger.info(f"Токен добавлен в blacklist, TTL: {ttl}s")
            return None, True
        except Exception as e:
            logger.error(f"Ошибка добавления токена в blacklist: {e}")
            return str(e), False
    
    def is_blacklisted(self, token: str) -> bool:
        """
        Проверить находится ли токен в blacklist
        
        Args:
            token: Строка JWT токена
            
        Returns:
            True если токен в blacklist
        """
        if self.redis_client is None:
            return False
        
        try:
            blacklist_key = f"token_blacklist:{token}"
            return self.redis_client.exists(blacklist_key)
        except Exception as e:
            logger.error(f"Ошибка проверки blacklist токена: {e}")
            return False
    
    def remove_from_blacklist(self, token: str) -> Tuple[Optional[str], bool]:
        """
        Удалить токен из blacklist
        
        Args:
            token: Строка JWT токена
            
        Returns:
            Кортеж (сообщение_об_ошибке, успех)
        """
        if self.redis_client is None:
            return None, True
        
        try:
            blacklist_key = f"token_blacklist:{token}"
            self.redis_client.delete(blacklist_key)
            return None, True
        except Exception as e:
            logger.error(f"Ошибка удаления токена из blacklist: {e}")
            return str(e), False
