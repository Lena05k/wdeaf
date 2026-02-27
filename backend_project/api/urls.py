from django.urls import path
from .views import email_signup, email_login, logout, get_current_user, health_check, RefreshTokenView

urlpatterns = [
    # Auth endpoints - login/signup with session
    path('auth/signup', email_signup, name='email_signup'),
    path('auth/login', email_login, name='email_login'),

    # Current user and logout (session or JWT)
    path('auth/me', get_current_user, name='get_current_user'),
    path('auth/logout', logout, name='logout'),

    # JWT token management
    path('auth/refresh', RefreshTokenView.as_view(), name='refresh_token'),

    # Health check
    path('health', health_check, name='health_check'),
]