"""
Telegram authentication service
Handles Telegram-based authentication
"""
from typing import Optional
from api.repositories import UserRepository
from api.models import User


class TelegramAuthService:
    """Service for Telegram-based authentication"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def find_or_create_user(
        self,
        telegram_id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None
    ):
        """
        Найти существующего Telegram пользователя или создать нового
        
        Args:
            telegram_id: Telegram ID пользователя
            first_name: Имя пользователя
            last_name: Фамилия (опционально)
            username: Telegram username (опционально)
            avatar_url: URL фото профиля (опционально)
            
        Returns:
            Объект User
        """
        user = self.user_repo.get_by_telegram_id(telegram_id)
        
        if user:
            # Обновляем данные существующего пользователя
            return self.user_repo.update(
                user,
                first_name=first_name,
                last_name=last_name,
                username=username,
                avatar_url=avatar_url
            )
        
        # Создаём нового Telegram пользователя
        return self.user_repo.create(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            avatar_url=avatar_url,
            auth_provider='telegram'
        )
