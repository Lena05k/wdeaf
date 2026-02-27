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
        Find existing phone user or create new one
        
        Args:
            phone: Phone number
            first_name: User first name
            last_name: User last name (optional)
            username: Username (optional)
            
        Returns:
            User object
        """
        user = self.user_repo.get_by_phone(phone)
        
        if user:
            # Update existing user info
            return self.user_repo.update(
                user,
                first_name=first_name,
                last_name=last_name,
                username=username
            )
        
        # Create new phone user
        return self.user_repo.create(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            username=username,
            auth_provider='phone'
        )
