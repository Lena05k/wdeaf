from rest_framework_simplejwt import authentication as jwt_authentication
from django.conf import settings
from rest_framework import authentication, exceptions as rest_exceptions


class UsersAuthentication(jwt_authentication.JWTAuthentication):
    """
    Custom JWT authentication
    Supports both header and cookie token extraction
    NO CSRF check - JWT in Authorization header is sufficient for API
    """
    def authenticate(self, request):
        # Пытаемся получить токен из заголовка
        header = self.get_header(request)

        # Если нет заголовка, пробуем cookie
        if header is None:
            raw_token = request.COOKIES.get(getattr(settings, 'SIMPLE_JWT', {}).get('AUTH_COOKIE', 'access_token'))
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        # Проверяем токен
        validated_token = self.get_validated_token(raw_token)

        # Проверяем blacklist
        if self.is_token_blacklisted(raw_token):
            raise rest_exceptions.AuthenticationFailed('Token has been revoked')

        # CSRF проверка не требуется - JWT токена в заголовке достаточно

        # Получаем пользователя из токена
        return self.get_user(validated_token), validated_token

    def is_token_blacklisted(self, token):
        """Проверка токена в Redis blacklist"""
        try:
            from .services.token_blacklist import is_token_blacklisted
            return is_token_blacklisted(token)
        except Exception as e:
            # Если Redis недоступен, считаем токен валидным
            return False
