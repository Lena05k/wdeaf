"""
Authentication views
Email-based signup/login/logout
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.services.auth import EmailAuthService
from api.services.token import JWTService, TokenBlacklistService
from api.serializers import EmailLoginRequestSerializer, EmailSignupRequestSerializer, UserSerializer
from api.utils.responses import AuthResponseBuilder
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=EmailSignupRequestSerializer,
        responses={
            201: openapi.Response(description='User registered successfully'),
            400: openapi.Response(description='Bad request'),
            409: openapi.Response(description='User already exists'),
        }
    )
    def post(self, request):
        """Register new user with email + password"""
        serializer = EmailSignupRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            auth_service = EmailAuthService()
            user = auth_service.register(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data.get('last_name')
            )
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)

        return AuthResponseBuilder.with_jwt(user, status_code=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=EmailLoginRequestSerializer,
        responses={
            200: openapi.Response(description='Login successful'),
            400: openapi.Response(description='Bad request'),
            401: openapi.Response(description='Invalid credentials'),
        }
    )
    def post(self, request):
        """Login with email + password"""
        serializer = EmailLoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_service = EmailAuthService()
        user = auth_service.authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        return AuthResponseBuilder.with_jwt(user)


class LogoutView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Logout successful'),
            401: openapi.Response(description='Token not found'),
        }
    )
    def post(self, request):
        """Logout and clear session + token cookie"""
        from django.conf import settings
        jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        access_token = request.COOKIES.get(jwt_settings.get('AUTH_COOKIE', 'access_token'))

        if not access_token:
            return Response(
                {'detail': 'Token not found in cookie. You may already be logged out.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Add token to Redis blacklist
        blacklist_service = TokenBlacklistService()
        try:
            jwt_service = JWTService()
            payload = jwt_service.decode_token(access_token)
            exp_timestamp = payload.get('exp')
            if exp_timestamp:
                expires_at = datetime.utcfromtimestamp(exp_timestamp)
            else:
                expires_at = datetime.utcnow() + timedelta(hours=24)
            
            blacklist_service.add_to_blacklist(access_token, expires_at)
        except Exception as e:
            logger.warning(f"Could not add token to blacklist: {e}")

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
