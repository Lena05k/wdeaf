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
        Find existing Telegram user or create new one
        
        Args:
            telegram_id: Telegram user ID
            first_name: User first name
            last_name: User last name (optional)
            username: Telegram username (optional)
            avatar_url: Profile photo URL (optional)
            
        Returns:
            User object
        """
        user = self.user_repo.get_by_telegram_id(telegram_id)
        
        if user:
            # Update existing user info
            return self.user_repo.update(
                user,
                first_name=first_name,
                last_name=last_name,
                username=username,
                avatar_url=avatar_url
            )
        
        # Create new Telegram user
        return self.user_repo.create(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            avatar_url=avatar_url,
            auth_provider='telegram'
        )
