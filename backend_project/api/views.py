from typing import Any, Optional
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from .models import User
from .serializers import (
    UserSerializer, AuthResponseSerializer,
    EmailLoginRequestSerializer, EmailSignupRequestSerializer,
    PhoneAuthRequestSerializer, RefreshTokenRequestSerializer
)
from .services import AuthService
import logging

logger = logging.getLogger(__name__)

# JWT utilities
def create_access_token(user_id: int, expires_hours: Optional[int] = None) -> str:
    exp = expires_hours or getattr(settings, 'JWT_EXPIRATION_HOURS', 24)
    payload = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=exp),
        'iat': datetime.utcnow(),
        'type': 'access',
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=getattr(settings, 'JWT_ALGORITHM', 'HS256'))

def create_refresh_token(user_id: int) -> str:
    payload = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow(),
        'type': 'refresh',
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=getattr(settings, 'JWT_ALGORITHM', 'HS256'))

def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[getattr(settings, 'JWT_ALGORITHM', 'HS256')])
    except jwt.InvalidTokenError as e:
        logger.error(f"❌ Token decode error: {e}")
        raise


@api_view(['POST'])
@permission_classes([AllowAny])
def email_signup(request: Request) -> Response:
    """Register new user with email + password"""
    serializer = EmailSignupRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = AuthService.register_email_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data.get('last_name')
        )
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Prepare response
    user_serializer = UserSerializer(user)
    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'user': user_serializer.data
    }

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_login(request: Request) -> Response:
    """Login with email + password"""
    serializer = EmailLoginRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = AuthService.authenticate_email_user(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password']
    )

    if not user:
        return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Prepare response
    user_serializer = UserSerializer(user)
    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'user': user_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def phone_auth(request: Request) -> Response:
    """Login/register via phone number"""
    serializer = PhoneAuthRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = AuthService.find_or_create_phone_user(
        phone=serializer.validated_data['phone'],
        first_name=serializer.validated_data['first_name'],
        last_name=serializer.validated_data.get('last_name'),
        username=serializer.validated_data.get('username')
    )

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Prepare response
    user_serializer = UserSerializer(user)
    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'user': user_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request: Request) -> Response:
    """Refresh access token using refresh token"""
    serializer = RefreshTokenRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        payload = decode_token(serializer.validated_data['refresh_token'])

        if payload.get('type') != 'refresh':
            return Response({'detail': 'Invalid token type'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = int(payload['sub'])
        user = User.objects.get(id=user_id)

        # Generate new tokens
        new_access_token = create_access_token(user.id)
        new_refresh_token = create_refresh_token(user.id)

        # Prepare response
        user_serializer = UserSerializer(user)
        response_data = {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token,
            'token_type': 'bearer',
            'user': user_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except jwt.InvalidTokenError:
        return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"❌ Refresh token error: {e}")
        return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_current_user(request: Request) -> Response:
    """Get current authenticated user"""
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """Health check endpoint"""
    return Response({
        'status': 'ok',
        'service': 'WDEAF Django Backend',
        'timestamp': timezone.now().isoformat()
    })
