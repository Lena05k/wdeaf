"""
User repository
Handles all database operations for User model
"""
from typing import Optional
from django.db.models import QuerySet
from api.models import User


class UserRepository:
    """Repository for User model operations"""
    
    def __init__(self):
        self.model = User
    
    # ─── Методы QuerySet ────────────────────────────────────────────

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()

    def filter(self, **kwargs) -> QuerySet[User]:
        return User.objects.filter(**kwargs)

    # ─── Методы получения ───────────────────────────────────────────

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return None
    
    def get_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone"""
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
    
    # ─── Методы проверки существования ─────────────────────────────

    def exists(self, **kwargs) -> bool:
        """Проверить существует ли пользователь"""
        return User.objects.filter(**kwargs).exists()

    def email_exists(self, email: str) -> bool:
        """Проверить зарегистрирован ли email"""
        return self.exists(email=email)

    def phone_exists(self, phone: str) -> bool:
        """Проверить зарегистрирован ли телефон"""
        return self.exists(phone=phone)

    def telegram_exists(self, telegram_id: int) -> bool:
        """Проверить зарегистрирован ли Telegram ID"""
        return self.exists(telegram_id=telegram_id)

    # ─── Методы создания ────────────────────────────────────────────

    def create(self, **kwargs) -> User:
        """Создать пользователя"""
        return User.objects.create(**kwargs)

    def create_user(self, email: str, password: str, **extra_fields) -> User:
        """Создать пользователя с хешированным паролем"""
        return User.objects.create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> User:
        """Создать суперпользователя"""
        return User.objects.create_superuser(email=email, password=password, **extra_fields)
    
    # ─── Методы обновления ──────────────────────────────────────────

    def update(self, user: User, **kwargs) -> User:
        """Обновить поля пользователя"""
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user

    # ─── Методы удаления ────────────────────────────────────────────

    def delete(self, user: User) -> None:
        """Удалить пользователя"""
        user.delete()

    # ─── Методы для провайдеров ─────────────────────────────────────

    def get_providers(self) -> QuerySet[User]:
        """Получить всех провайдеров (is_provider=True)"""
        return User.objects.filter(is_provider=True).order_by('-created_at')

    def create_provider(self, email: str, password: str, **extra_fields) -> User:
        """Создать пользователя-провайдера"""
        extra_fields['is_provider'] = True
        extra_fields['auth_provider'] = 'email'
        return self.create_user(email=email, password=password, **extra_fields)
