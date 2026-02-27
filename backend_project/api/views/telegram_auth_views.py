"""
Telegram authentication views
Handles Telegram WebApp data validation and user authentication
Similar to functions/auth.py telegram auth implementation
"""
import hashlib
import hmac
import logging
from datetime import datetime
from urllib.parse import parse_qs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from ..serializers import TelegramAuthRequestSerializer, AuthResponseSerializer
from ..services import AuthService
from .jwt_utils import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)


class TelegramAuthView(APIView):
    """
    Telegram WebApp authentication
    Validates Telegram WebApp data and creates/authenticates user
    Similar to functions/auth.py phone_login endpoint
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=TelegramAuthRequestSerializer,
        responses={
            200: AuthResponseSerializer,
            400: openapi.Response(description='Invalid Telegram data'),
            401: openapi.Response(description='Invalid hash or expired data'),
        }
    )
    def post(self, request):
        """
        Authenticate user with Telegram WebApp data
        
        Request body:
        - id: Telegram user ID
        - first_name: User's first name
        - last_name: User's last name (optional)
        - username: Telegram username (optional)
        - photo_url: Profile photo URL (optional)
        - auth_date: Unix timestamp of authorization
        - hash: HMAC-SHA256 signature
        
        Returns:
        - JWT access_token and refresh_token
        - User information
        """
        # Get Telegram data from request
        telegram_data = request.data
        
        # Validate required fields
        required_fields = ['id', 'first_name', 'auth_date', 'hash']
        for field in required_fields:
            if field not in telegram_data:
                return Response(
                    {'detail': f'Missing required field: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Validate hash
        bot_token = getattr(settings, 'BOT_TOKEN', None)
        if not bot_token:
            logger.error("BOT_TOKEN not configured in settings")
            return Response(
                {'detail': 'Server configuration error: BOT_TOKEN not set'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        if not self.validate_telegram_data(telegram_data, bot_token):
            return Response(
                {'detail': 'Invalid Telegram data hash'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check auth_date (not older than 24 hours)
        auth_date = int(telegram_data.get('auth_date', 0))
        current_time = int(datetime.now().timestamp())
        if current_time - auth_date > 86400:  # 24 hours
            return Response(
                {'detail': 'Telegram data expired'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get or create user
        telegram_id = int(telegram_data['id'])
        first_name = telegram_data.get('first_name', '')
        last_name = telegram_data.get('last_name', '')
        username = telegram_data.get('username', '')
        photo_url = telegram_data.get('photo_url', '')
        
        try:
            user = AuthService.find_or_create_telegram_user(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                avatar_url=photo_url
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

    @staticmethod
    def validate_telegram_data(data: dict, bot_token: str) -> bool:
        """
        Validate Telegram WebApp data hash
        Similar to functions/auth.py validate_telegram_data
        """
        # Extract hash from data
        received_hash = data.get('hash')
        if not received_hash:
            return False
        
        # Create data check string (all fields except hash, sorted)
        data_check_arr = []
        for key, value in data.items():
            if key != 'hash':
                data_check_arr.append(f"{key}={value}")
        data_check_arr.sort()
        data_check_string = '\n'.join(data_check_arr)
        
        # Create secret key (HMAC-SHA256 of "WebAppData" with bot_token)
        secret_key = hmac.new(
            b"WebAppData",
            bot_token.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # Calculate hash (HMAC-SHA256 of data_check_string with secret_key)
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Compare hashes
        return hmac.compare_digest(received_hash, calculated_hash)
