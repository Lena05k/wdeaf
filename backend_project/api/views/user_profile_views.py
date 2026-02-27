"""
User profile management views
Handles user profile update and deletion
Similar to functions/ user model operations
"""
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import UserUpdateSerializer, UserSerializer
from ..models import User

logger = logging.getLogger(__name__)


class UserUpdateView(APIView):
    """
    Update user profile
    Allows users to update their own profile information
    CSRF exempt for API usage
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={
            200: UserSerializer,
            400: openapi.Response(description='Invalid data'),
            404: openapi.Response(description='User not found'),
        }
    )
    @csrf_exempt
    def put(self, request):
        """
        Update user profile
        
        Request body:
        - first_name: User's first name (optional)
        - last_name: User's last name (optional)
        - username: Username (optional)
        - avatar_url: Profile photo URL (optional)
        
        Returns:
        - Updated user information
        """
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={
            200: UserSerializer,
            400: openapi.Response(description='Invalid data'),
            404: openapi.Response(description='User not found'),
        }
    )
    @csrf_exempt
    def patch(self, request):
        """
        Partial update user profile
        
        Request body (all fields optional):
        - first_name: User's first name
        - last_name: User's last name
        - username: Username
        - avatar_url: Profile photo URL
        
        Returns:
        - Updated user information
        """
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    """
    Delete user account
    Allows users to delete their own account
    CSRF exempt for API usage
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Account deleted successfully'),
            404: openapi.Response(description='User not found'),
        }
    )
    @csrf_exempt
    def delete(self, request):
        """
        Delete user account
        
        This action is irreversible!
        
        Returns:
        - Success message
        """
        user = request.user
        
        # Log deletion for audit
        logger.info(f"User account deletion requested: {user.id} ({user.email or user.phone or user.telegram_id})")
        
        # Store user info for response (before deletion)
        user_id = user.id
        
        # Delete user
        user.delete()
        
        logger.info(f"User account deleted: {user_id}")
        
        return Response(
            {'detail': 'Account deleted successfully'},
            status=status.HTTP_200_OK
        )
