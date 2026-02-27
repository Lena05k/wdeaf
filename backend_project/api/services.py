from typing import Optional
from django.contrib.auth.hashers import make_password, check_password
from .models import User


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