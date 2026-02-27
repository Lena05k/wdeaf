from typing import Optional
from django.contrib.auth.hashers import make_password, check_password
from api.models import User


class AuthService:
    """
    Service class for handling authentication-related operations
    """

    @staticmethod
    def register_email_user(
        email: str,
        password: str,
        first_name: str,
        last_name: Optional[str] = None
    ) -> User:
        """
        Register a new user with email and password
        """
        if User.objects.filter(email=email).exists():
            raise ValueError("User with this email already exists")

        user = User.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            auth_provider='email'
        )

        return user

    @staticmethod
    def authenticate_email_user(email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if not check_password(password, user.password):
            return None

        return user

    @staticmethod
    def find_or_create_telegram_user(
        telegram_id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None
    ) -> User:
        """
        Find or create Telegram user
        Similar to functions/services/auth_service.py find_or_create_telegram_user
        """
        try:
            user = User.objects.get(telegram_id=telegram_id)
            # Update user info if changed
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.avatar_url = avatar_url
            user.save()
            return user
        except User.DoesNotExist:
            # Create new Telegram user
            user = User.objects.create(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                avatar_url=avatar_url,
                auth_provider='telegram'
            )
            return user