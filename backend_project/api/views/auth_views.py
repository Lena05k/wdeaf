"""
Authentication views for user login, signup and logout
JWT-only implementation (no Django session)
Similar to MarsStationBackend
"""
import logging
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from ..serializers import (
    UserSerializer, EmailLoginRequestSerializer, EmailSignupRequestSerializer
)
from ..services import AuthService
from .jwt_utils import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # No session auth, only JWT

    @swagger_auto_schema(
        request_body=EmailSignupRequestSerializer,
        responses={
            201: openapi.Response(
                description='User registered successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'token_type': openapi.Schema(type=openapi.TYPE_STRING, description='Token type (bearer)'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='User object'),
                    }
                )
            ),
            400: openapi.Response(description='Bad request'),
            409: openapi.Response(description='User already exists'),
        }
    )
    def post(self, request):
        """
        Register new user with email + password
        Returns ONLY JWT token in cookie (no session)
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

        # Create JWT tokens ONLY (no Django session)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response(status=status.HTTP_201_CREATED)
        # Set ONLY access_token in cookie (no sessionid, no csrftoken)
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
    authentication_classes = []  # No session auth, only JWT

    @swagger_auto_schema(
        request_body=EmailLoginRequestSerializer,
        responses={
            200: openapi.Response(
                description='Login successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'token_type': openapi.Schema(type=openapi.TYPE_STRING, description='Token type (bearer)'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='User object'),
                    }
                )
            ),
            400: openapi.Response(description='Bad request'),
            401: openapi.Response(description='Invalid credentials'),
        }
    )
    def post(self, request):
        """
        Login with email + password
        Returns ONLY JWT token in cookie (no session)
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

        # Create JWT tokens ONLY (no Django session)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response(status=status.HTTP_200_OK)
        # Set ONLY access_token in cookie (no sessionid, no csrftoken)
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
    Logout view - JWT only (like MarsStationBackend)
    Clear access_token cookie, add token to Redis blacklist
    """
    authentication_classes = []  # No CSRF check
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Logout successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Additional message'),
                    }
                )
            ),
            401: openapi.Response(description='Already logged out or no token'),
        }
    )
    def post(self, request):
        """
        Logout - clear access_token cookie only
        Return error if already logged out (no token)
        """
        from .jwt_utils import decode_token
        from ..services.token_blacklist import add_token_to_blacklist

        # Get token from cookie
        jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        access_token = request.COOKIES.get(jwt_settings.get('AUTH_COOKIE', 'access_token'))

        # Проверка наличия токена
        if access_token is None:
            return Response(
                {
                    'detail': 'Already logged out',
                    'message': 'No access token found in cookie'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Add token to Redis blacklist
        error_message = None
        try:
            decoded = decode_token(access_token)
            exp_timestamp = decoded.get('exp')
            if exp_timestamp:
                expires_at = datetime.utcfromtimestamp(exp_timestamp)
            else:
                expires_at = datetime.utcnow() + timedelta(hours=24)

            err, success = add_token_to_blacklist(access_token, expires_at)
            if err:
                error_message = err
        except Exception as e:
            error_message = str(e)

        response = Response(status=status.HTTP_200_OK)

        # Clear ONLY access_token cookie (no sessionid, no csrftoken)
        response.delete_cookie(
            key=jwt_settings.get('AUTH_COOKIE', 'access_token'),
            path=jwt_settings.get('AUTH_COOKIE_PATH', '/')
        )

        response.data = {
            'detail': 'Successfully logged out',
            'message': 'Access token cleared and blacklisted'
        }

        if error_message:
            response.data['error_message'] = error_message

        return response


# Function-based views for URL routing
email_signup = SignupView.as_view()
email_login = LoginView.as_view()
logout = LogoutView.as_view()
