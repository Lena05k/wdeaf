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
    
    # ─── QuerySet methods ───────────────────────────────────────────
    
    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()
    
    def filter(self, **kwargs) -> QuerySet[User]:
        return User.objects.filter(**kwargs)
    
    # ─── Get methods ────────────────────────────────────────────────
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
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
    
    # ─── Check methods ──────────────────────────────────────────────
    
    def exists(self, **kwargs) -> bool:
        """Check if user exists"""
        return User.objects.filter(**kwargs).exists()
    
    def email_exists(self, email: str) -> bool:
        """Check if email is already registered"""
        return self.exists(email=email)
    
    def phone_exists(self, phone: str) -> bool:
        """Check if phone is already registered"""
        return self.exists(phone=phone)
    
    def telegram_exists(self, telegram_id: int) -> bool:
        """Check if Telegram ID is already registered"""
        return self.exists(telegram_id=telegram_id)
    
    # ─── Create methods ─────────────────────────────────────────────
    
    def create(self, **kwargs) -> User:
        """Create new user"""
        return User.objects.create(**kwargs)
    
    def create_user(self, email: str, password: str, **extra_fields) -> User:
        """Create user with hashed password"""
        return User.objects.create_user(email=email, password=password, **extra_fields)
    
    def create_superuser(self, email: str, password: str, **extra_fields) -> User:
        """Create superuser"""
        return User.objects.create_superuser(email=email, password=password, **extra_fields)
    
    # ─── Update methods ─────────────────────────────────────────────
    
    def update(self, user: User, **kwargs) -> User:
        """Update user fields"""
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user
    
    # ─── Delete methods ─────────────────────────────────────────────
    
    def delete(self, user: User) -> None:
        """Delete user"""
        user.delete()
    
    # ─── Provider specific methods ──────────────────────────────────
    
    def get_providers(self) -> QuerySet[User]:
        """Get all providers (is_provider=True)"""
        return User.objects.filter(is_provider=True).order_by('-created_at')
    
    def create_provider(self, email: str, password: str, **extra_fields) -> User:
        """Create provider user"""
        extra_fields['is_provider'] = True
        extra_fields['auth_provider'] = 'email'
        return self.create_user(email=email, password=password, **extra_fields)
