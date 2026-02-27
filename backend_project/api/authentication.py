from rest_framework_simplejwt import authentication as jwt_authentication
from django.conf import settings
from rest_framework import authentication, exceptions as rest_exceptions


def enforce_csrf(request):
    """
    Enforce CSRF check for JWT authentication
    Similar to MarsStationBackend implementation
    """
    check = authentication.CSRFCheck(request)
    reason = check.process_view(request, None, (), {})
    
    if reason:
        raise rest_exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class UsersAuthentication(jwt_authentication.JWTAuthentication):
    """
    Custom JWT authentication with CSRF check
    Supports both header and cookie token extraction
    Similar to MarsStationBackend implementation
    """
    def authenticate(self, request):
        # Try to get token from header first
        header = self.get_header(request)

        # If no header, try cookie
        if header is None:
            raw_token = request.COOKIES.get(getattr(settings, 'SIMPLE_JWT', {}).get('AUTH_COOKIE', 'access_token'))
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        # Validate token
        validated_token = self.get_validated_token(raw_token)

        # Check if token is blacklisted (like MarsStationBackend)
        if self.is_token_blacklisted(raw_token):
            raise rest_exceptions.AuthenticationFailed('Token has been revoked')

        # Enforce CSRF check
        enforce_csrf(request)

        # Get user from token
        return self.get_user(validated_token), validated_token

    def is_token_blacklisted(self, token):
        """Check if token is in Redis blacklist"""
        try:
            from .services.token_blacklist import is_token_blacklisted
            return is_token_blacklisted(token)
        except Exception as e:
            # If Redis is unavailable, assume token is valid
            return False
