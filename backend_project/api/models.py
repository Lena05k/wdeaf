from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from typing import Optional


class UserManager(BaseUserManager):
    """Custom manager for User model"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=32, unique=True, null=True, blank=True, db_index=True)
    avatar_url = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=20,
        default='telegram',
        choices=[
            ('telegram', 'Telegram'),
            ('email', 'Email'),
            ('phone', 'Phone'),
        ],
        help_text="telegram | email | phone"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(fields=['telegram_id'], name='ix_users_telegram_id'),
            models.Index(fields=['email'], name='ix_users_email'),
            models.Index(fields=['created_at'], name='ix_users_created_at'),
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name or ''}".strip()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "is_provider": self.is_provider,
            "auth_provider": self.auth_provider,
        }
