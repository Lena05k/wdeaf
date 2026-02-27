from rest_framework import authentication
from django.contrib.auth import authenticate


class SessionAuthenticationNoCSRF(authentication.SessionAuthentication):
    """
    Session authentication without CSRF check
    For API usage where CSRF tokens are not practical
    """
    def enforce_csrf(self, request):
        # Skip CSRF check for API usage
        return
