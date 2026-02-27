"""
Authentication views for user login, signup and logout
"""
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login as django_login, logout as django_logout
from ..serializers import (
    UserSerializer, AuthResponseSerializer,
    EmailLoginRequestSerializer, EmailSignupRequestSerializer
)
from ..services import AuthService
from .jwt_utils import create_access_token, create_refresh_token


@api_view(['POST'])
@permission_classes([AllowAny])
def email_signup(request: Request) -> Response:
    """
    Register new user with email + password and create session
    
    Expects: { "email": "...", "password": "...", "first_name": "...", "last_name": "..." }
    Returns: { "access_token": "...", "refresh_token": "...", "token_type": "bearer", "user": {...} }
    """
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

    # Create Django session
    django_login(request, user)

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
    """
    Login with email + password and create session
    
    Expects: { "email": "...", "password": "..." }
    Returns: { "access_token": "...", "refresh_token": "...", "token_type": "bearer", "user": {...} }
    """
    serializer = EmailLoginRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = AuthService.authenticate_email_user(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password']
    )

    if not user:
        return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    # Create Django session
    django_login(request, user)

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
@permission_classes([IsAuthenticated])
def logout(request: Request) -> Response:
    """
    Logout and clear session
    
    Requires: Authentication (session or JWT)
    Returns: { "detail": "Successfully logged out" }
    """
    django_logout(request)
    return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
