"""
Phone authentication service
Handles phone-based authentication
"""
from typing import Optional
from api.repositories import UserRepository
from api.models import User


class PhoneAuthService:
    """Service for phone-based authentication"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def find_or_create_user(
        self,
        phone: str,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None
    ):
        """
        Найти существующего пользователя по телефону или создать нового
        
        Args:
            phone: Номер телефона
            first_name: Имя пользователя
            last_name: Фамилия (опционально)
            username: Username (опционально)
            
        Returns:
            Объект User
        """
        user = self.user_repo.get_by_phone(phone)
        
        if user:
            # Обновляем данные существующего пользователя
            return self.user_repo.update(
                user,
                first_name=first_name,
                last_name=last_name,
                username=username
            )
        
        # Создаём нового пользователя по телефону
        return self.user_repo.create(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            username=username,
            auth_provider='phone'
        )
