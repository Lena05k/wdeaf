"""
Phone authentication views
Handles phone-based authentication (SMS verification temporarily disabled)
Similar to functions/auth.py phone_login endpoint
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import PhoneAuthRequestSerializer, AuthResponseSerializer
from ..services import AuthService
from .jwt_utils import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)


class PhoneAuthView(APIView):
    """
    Phone number authentication
    Login or register user via phone number
    Similar to functions/auth.py phone_login endpoint
    
    Note: SMS verification is temporarily disabled for initial rollout.
    Phone number is used directly without verification code.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=PhoneAuthRequestSerializer,
        responses={
            200: AuthResponseSerializer,
            400: openapi.Response(description='Invalid phone number format'),
            409: openapi.Response(description='Phone already registered with different data'),
        }
    )
    def post(self, request):
        """
        Login/register via phone number
        
        Request body:
        - phone: Phone number in format +7XXXXXXXXXX (10-15 digits)
        - first_name: User's first name
        - last_name: User's last name (optional)
        - username: Username (optional)
        
        Returns:
        - JWT access_token and refresh_token
        - User information
        
        Note: SMS verification is currently disabled
        """
        serializer = PhoneAuthRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get validated data
        phone = serializer.validated_data['phone']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data.get('last_name', '')
        username = serializer.validated_data.get('username', '')
        
        # Find or create user
        try:
            user = AuthService.find_or_create_phone_user(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                username=username
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_409_CONFLICT
            )
        
        # Generate JWT tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'user': {
                'id': user.id,
                'telegram_id': user.telegram_id,
                'email': user.email,
                'phone': user.phone,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'avatar_url': user.avatar_url,
                'is_provider': user.is_provider,
                'auth_provider': user.auth_provider,
            }
        }, status=status.HTTP_200_OK)
