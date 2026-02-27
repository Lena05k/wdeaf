"""
Response builder for consistent API responses
DRY - Don't Repeat Yourself
"""
from rest_framework.response import Response
from rest_framework import status
from api.services import JWTService
from api.serializers import UserSerializer


class AuthResponseBuilder:
    """Builder for authentication responses with JWT tokens"""
    
    @staticmethod
    def with_jwt(user, status_code=status.HTTP_200_OK) -> Response:
        """
        Create response with JWT tokens
        
        Args:
            user: User object
            status_code: HTTP status code
            
        Returns:
            Response with JWT tokens and user data
        """
        jwt_service = JWTService()
        access_token = jwt_service.create_access_token(user.id)
        refresh_token = jwt_service.create_refresh_token(user.id)
        
        response = Response(status=status_code)
        
        # Set tokens in cookies
        from django.conf import settings
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
    
    @staticmethod
    def success(data=None, message='Success', status_code=status.HTTP_200_OK) -> Response:
        """
        Create success response
        
        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code
            
        Returns:
            Response
        """
        response_data = {'detail': message}
        if data:
            response_data.update(data)
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message='Error', status_code=status.HTTP_400_BAD_REQUEST) -> Response:
        """
        Create error response
        
        Args:
            message: Error message
            status_code: HTTP status code
            
        Returns:
            Response
        """
        return Response({'detail': message}, status=status_code)
    
    @staticmethod
    def validation_error(errors, status_code=status.HTTP_400_BAD_REQUEST) -> Response:
        """
        Create validation error response
        
        Args:
            errors: Validation errors dict
            status_code: HTTP status code
            
        Returns:
            Response
        """
        return Response(errors, status=status_code)
