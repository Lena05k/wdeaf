"""
Provider authentication service
Handles provider registration
"""
from typing import Optional
from api.repositories import UserRepository
from api.models import User


class ProviderAuthService:
    """Service for provider authentication"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: Optional[str] = None,
        phone: Optional[str] = None
    ):
        """
        Register new service provider
        
        Args:
            email: Provider email
            password: Plain text password
            first_name: Provider name
            last_name: Provider surname (optional)
            phone: Provider phone (optional)
            
        Returns:
            User object (is_provider=True)
            
        Raises:
            ValueError: If email already registered
        """
        if self.user_repo.email_exists(email):
            raise ValueError("Provider with this email already exists")
        
        return self.user_repo.create_provider(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
