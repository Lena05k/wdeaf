"""
Health check and system views
"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


@api_view(['GET'])
@permission_classes([AllowAny])
@swagger_auto_schema(
    responses={
        200: openapi.Response(
            description='Service health status',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Service status'),
                    'service': openapi.Schema(type=openapi.TYPE_STRING, description='Service name'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, description='Current timestamp'),
                }
            )
        ),
    }
)
def health_check(request: Request) -> Response:
    """
    Health check endpoint
    
    Returns: { "status": "ok", "service": "...", "timestamp": "..." }
    """
    return Response({
        'status': 'ok',
        'service': 'WDEAF Django Backend',
        'timestamp': timezone.now().isoformat()
    }, status=status.HTTP_200_OK)
