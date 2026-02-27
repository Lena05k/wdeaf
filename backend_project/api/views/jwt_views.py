"""
JWT token management views
Handles token refresh and validation
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import RefreshTokenRequestSerializer
from ..services import AuthService
from .jwt_utils import create_access_token, create_refresh_token, decode_token
from ..models import User


class RefreshTokenView(APIView):
    """
    Refresh JWT access token using refresh token
    Similar to functions/auth.py refresh_token endpoint
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RefreshTokenRequestSerializer,
        responses={
            200: openapi.Response(
                description='Token refreshed successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='New JWT access token'),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='New JWT refresh token'),
                        'token_type': openapi.Schema(type=openapi.TYPE_STRING, description='Token type (bearer)'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='User object'),
                    }
                )
            ),
            400: openapi.Response(description='Invalid token'),
            401: openapi.Response(description='Token expired or invalid'),
            404: openapi.Response(description='User not found'),
        }
    )
    def post(self, request):
        """
        Refresh access token using refresh token
        
        Request body:
        - refresh_token: JWT refresh token
        
        Returns:
        - New access_token and refresh_token
        - User information
        """
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Decode and validate refresh token
        try:
            payload = decode_token(refresh_token)
        except Exception as e:
            return Response(
                {'detail': f'Invalid token: {str(e)}'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check token type
        if payload.get('token_type') != 'refresh':
            return Response(
                {'detail': 'Invalid token type. Expected refresh token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get user ID from token
        try:
            user_id = int(payload.get('sub'))
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid user ID in token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get user from database
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generate new tokens
        new_access_token = create_access_token(user.id)
        new_refresh_token = create_refresh_token(user.id)
        
        return Response({
            'access_token': new_access_token,
            'refresh_token': new_refresh_token,
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
