"""
Email authentication service
Handles email-based registration and login
"""
from typing import Optional
from django.contrib.auth.hashers import check_password
from api.repositories import UserRepository
from api.models import User


class EmailAuthService:
    """Service for email-based authentication"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def register(self, email: str, password: str, first_name: str, last_name: Optional[str] = None):
        """
        Register new user with email and password
        
        Args:
            email: User email
            password: Plain text password
            first_name: User first name
            last_name: User last name (optional)
            
        Returns:
            User object
            
        Raises:
            ValueError: If email already registered
        """
        if self.user_repo.email_exists(email):
            raise ValueError("User with this email already exists")
        
        return self.user_repo.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            auth_provider='email'
        )
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            User object if authenticated, None otherwise
        """
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        
        if not check_password(password, user.password):
            return None
        
        return user
