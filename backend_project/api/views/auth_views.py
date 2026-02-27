"""
Authentication views for user login, signup and logout
Similar to MarsStationBackend implementation
"""
import logging
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import login as django_login, logout as django_logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..serializers import (
    UserSerializer, EmailLoginRequestSerializer, EmailSignupRequestSerializer
)
from ..services import AuthService
from .jwt_utils import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        """
        Register new user with email + password and create session
        Returns JWT token in cookie (like MarsStationBackend)
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

        django_login(request, user)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response(status=status.HTTP_201_CREATED)
        # Set token in cookie (like MarsStationBackend)
        jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        response.set_cookie(
            key=jwt_settings.get('AUTH_COOKIE', 'access_token'),
            value=access_token,
            httponly=jwt_settings.get('AUTH_COOKIE_HTTPONLY', True),
            path=jwt_settings.get('AUTH_COOKIE_PATH', '/'),
            samesite=jwt_settings.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            secure=jwt_settings.get('AUTH_COOKIE_SECURE', False)
        )

        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'user': UserSerializer(user).data
        }
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        """
        Login with email + password and create session
        Returns JWT token in cookie (like MarsStationBackend)
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

        django_login(request, user)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response(status=status.HTTP_200_OK)
        # Set token in cookie (like MarsStationBackend)
        jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        response.set_cookie(
            key=jwt_settings.get('AUTH_COOKIE', 'access_token'),
            value=access_token,
            httponly=jwt_settings.get('AUTH_COOKIE_HTTPONLY', True),
            path=jwt_settings.get('AUTH_COOKIE_PATH', '/'),
            samesite=jwt_settings.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            secure=jwt_settings.get('AUTH_COOKIE_SECURE', False)
        )

        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'user': UserSerializer(user).data
        }
        return response


class LogoutView(APIView):
    """
    Logout view - like MarsStationBackend
    Token from cookie, add to Redis blacklist, clear cookie
    """
    authentication_classes = []  # No CSRF check
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Logout - like MarsStationBackend implementation
        """
        from .jwt_utils import decode_token
        from ..services.token_blacklist import add_token_to_blacklist
        
        # Get token from cookie (like MarsStationBackend)
        jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        access_token = request.COOKIES.get(jwt_settings.get('AUTH_COOKIE', 'access_token'))

        # Проверка наличия токена
        if access_token is None:
            return Response(
                {'detail': 'Token not found in cookie. You may already be logged out.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Добавление токена в черный список в Redis (like MarsStationBackend)
        try:
            decoded = decode_token(access_token)
            exp_timestamp = decoded.get('exp')
            if exp_timestamp:
                expires_at = datetime.utcfromtimestamp(exp_timestamp)
            else:
                expires_at = datetime.utcnow() + timedelta(hours=24)
            
            error_message, success = add_token_to_blacklist(access_token, expires_at)
        except Exception as e:
            error_message = str(e)
            success = False

        response = Response(status=status.HTTP_200_OK)

        # Удаление куки с токеном (like MarsStationBackend)
        response.delete_cookie(
            key=jwt_settings.get('AUTH_COOKIE', 'access_token'),
            path=jwt_settings.get('AUTH_COOKIE_PATH', '/')
        )

        response.data = {
            'detail': 'Successfully logged out',
            'message': 'Token cleared'
        }

        # Добавляем error_message, если есть ошибка
        if error_message:
            response.data['error_message'] = error_message

        return response


# Function-based views for URL routing
email_signup = SignupView.as_view()
email_login = LoginView.as_view()
logout = LogoutView.as_view()
