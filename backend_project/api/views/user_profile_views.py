"""
User profile management views
"""
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.authentication import UsersAuthentication
from api.serializers import UserUpdateSerializer, UserSerializer
from api.repositories import UserRepository

logger = logging.getLogger(__name__)


class UserUpdateView(APIView):
    authentication_classes = [UsersAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer, 400: openapi.Response(description='Invalid data')}
    )
    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer, 400: openapi.Response(description='Invalid data')}
    )
    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    authentication_classes = [UsersAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: openapi.Response(description='Account deleted successfully')})
    def delete(self, request):
        user = request.user
        logger.info(f"User account deletion requested: {user.id}")
        
        user_id = user.id
        user.delete()
        logger.info(f"User account deleted: {user_id}")

        response = Response({'detail': 'Account deleted successfully'}, status=status.HTTP_200_OK)
        
        jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        response.delete_cookie(key=jwt_settings.get('AUTH_COOKIE', 'access_token'), path='/')
        response.delete_cookie(key='refresh_token', path='/')
        return response
