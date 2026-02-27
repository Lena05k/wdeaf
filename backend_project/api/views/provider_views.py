"""
Provider authentication and management views
For service providers (is_provider=True)
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from ..serializers import (
    ProviderSignupRequestSerializer,
    ProviderListSerializer,
    UserSerializer
)
from ..services import AuthService
from ..models import User
from .jwt_utils import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)


class ProviderSignupView(APIView):
    """
    Provider registration
    Register as a service provider with additional information
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=ProviderSignupRequestSerializer,
        responses={
            201: openapi.Response(
                description='Provider registered successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'token_type': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                    }
                )
            ),
            400: openapi.Response(description='Bad request'),
            409: openapi.Response(description='Provider already exists'),
        }
    )
    def post(self, request):
        """
        Register as a service provider
        
        Request body:
        - email: Provider email
        - password: Password (min 8 characters)
        - first_name: Provider name
        - last_name: Provider surname (optional)
        - phone: Provider phone number
        - company_name: Company name (optional)
        
        Returns:
        - JWT tokens
        - Provider user information
        """
        serializer = ProviderSignupRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create provider user
            user = AuthService.register_provider_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data.get('last_name'),
                phone=serializer.validated_data.get('phone'),
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_409_CONFLICT
            )
        
        # Generate JWT tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class ProviderListView(APIView):
    """
    Get list of service providers
    Returns paginated list of providers
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size'
            ),
        ],
        responses={
            200: openapi.Response(
                description='List of providers',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'next': openapi.Schema(type=openapi.TYPE_STRING),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(schema=ProviderListSerializer)
                        ),
                    }
                )
            ),
        }
    )
    def get(self, request):
        """
        Get list of service providers
        
        Query parameters:
        - page: Page number (default: 1)
        - page_size: Items per page (default: 20)
        
        Returns:
        - Paginated list of providers
        """
        # Get pagination parameters
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
        except (ValueError, TypeError):
            page = 1
            page_size = 20
        
        # Limit page_size
        page_size = min(page_size, 100)
        
        # Get providers
        providers = User.objects.filter(is_provider=True).order_by('-created_at')
        
        # Paginate
        start = (page - 1) * page_size
        end = start + page_size
        providers_page = providers[start:end]
        
        # Serialize
        serializer = ProviderListSerializer(providers_page, many=True)
        
        return Response({
            'count': providers.count(),
            'next': f'?page={page + 1}&page_size={page_size}' if end < providers.count() else None,
            'previous': f'?page={page - 1}&page_size={page_size}' if page > 1 else None,
            'results': serializer.data
        }, status=status.HTTP_200_OK)
