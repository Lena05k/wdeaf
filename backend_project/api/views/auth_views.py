"""
Authentication views for user login, signup and logout
Similar to MarsStationBackend implementation
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import login as django_login, logout as django_logout
from django.conf import settings
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
    Logout view - uses session authentication
    CSRF exempt for API usage (like login/signup)
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Logout and clear session + token cookie
        Add token to Redis blacklist (like MarsStationBackend)
        """
        from .jwt_utils import decode_token
        from ..services.token_blacklist import add_token_to_blacklist
        from datetime import datetime, timedelta
        
        # Get token from cookie (like MarsStationBackend)
        jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        access_token = request.COOKIES.get(jwt_settings.get('AUTH_COOKIE', 'access_token'))

        if access_token is None:
            return Response(
                {'detail': 'Token not found in cookie. You may already be logged out.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Add token to Redis blacklist (like MarsStationBackend)
        try:
            decoded = decode_token(access_token)
            exp_timestamp = decoded.get('exp')
            if exp_timestamp:
                expires_at = datetime.utcfromtimestamp(exp_timestamp)
            else:
                expires_at = datetime.utcnow() + timedelta(hours=24)
            
            error_message, success = add_token_to_blacklist(access_token, expires_at)
            if error_message:
                logger.warning(f"Token blacklist warning: {error_message}")
        except Exception as e:
            logger.warning(f"Could not add token to blacklist: {e}")

        # Logout user
        if request.user.is_authenticated:
            django_logout(request)

        response = Response(status=status.HTTP_200_OK)
        # Clear token cookie
        response.delete_cookie(
            key=jwt_settings.get('AUTH_COOKIE', 'access_token'),
            path=jwt_settings.get('AUTH_COOKIE_PATH', '/')
        )
        response.data = {
            'detail': 'Successfully logged out',
            'message': 'Token cleared and blacklisted'
        }
        return response


# Function-based views for URL routing
email_signup = SignupView.as_view()
email_login = LoginView.as_view()
logout = LogoutView.as_view()
