"""
Health check and system views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


@api_view(['GET'])
@permission_classes([AllowAny])
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
