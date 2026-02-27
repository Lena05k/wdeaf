"""
Authentication views for user login, signup and logout
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..authentication import SessionAuthenticationNoCSRF
from ..serializers import (
    UserSerializer, EmailLoginRequestSerializer, EmailSignupRequestSerializer
)
from ..services import AuthService
from .jwt_utils import create_access_token, create_refresh_token


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthenticationNoCSRF]

    def post(self, request):
        """
        Register new user with email + password and create session
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

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthenticationNoCSRF]

    def post(self, request):
        """
        Login with email + password and create session
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

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Logout view - CSRF exempt, uses session authentication without CSRF
    """
    authentication_classes = [SessionAuthenticationNoCSRF]
    
    def post(self, request):
        """
        Logout and clear session
        """
        if request.user.is_authenticated:
            django_logout(request)
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)


# Function-based views for URL routing with csrf_exempt
email_signup = csrf_exempt(SignupView.as_view())
email_login = csrf_exempt(LoginView.as_view())
logout = csrf_exempt(LogoutView.as_view())
