from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class AuthService:
    """
    Service class for handling authentication-related operations
    """
    
    @staticmethod
    def register_email_user(email, password, first_name, last_name=None):
        """
        Register a new user with email and password
        """
        # Validate input
        if User.objects.filter(email=email).exists():
            raise ValueError("User with this email already exists")
        
        # Create user
        user = User.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            auth_provider='email'
        )
        
        return user
    
    @staticmethod
    def authenticate_email_user(email, password):
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
    def find_or_create_phone_user(phone, first_name, last_name=None, username=None):
        """
        Find existing user by phone or create new one
        """
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'auth_provider': 'phone'
            }
        )
        
        if not created and not user.is_active:
            # Reactivate inactive user
            user.is_active = True
            user.save()
            
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None