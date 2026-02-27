"""
User profile views
"""
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from ..serializers import UserSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request: Request) -> Response:
    """
    Get current authenticated user information
    
    Requires: Authentication (session or JWT)
    Returns: User object { "id": ..., "email": "...", "first_name": "...", ... }
    """
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)
