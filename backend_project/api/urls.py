from django.urls import path
from .views import email_signup, email_login, logout, get_current_user, health_check, RefreshTokenView, TelegramAuthView, PhoneAuthView, UserUpdateView, UserDeleteView, ProviderSignupView, ProviderListView

urlpatterns = [
    # Auth endpoints - login/signup with session
    path('auth/signup', email_signup, name='email_signup'),
    path('auth/login', email_login, name='email_login'),

    # Current user and logout (session or JWT)
    path('auth/me', get_current_user, name='get_current_user'),
    path('auth/logout', logout, name='logout'),

    # User profile management
    path('auth/me/update', UserUpdateView.as_view(), name='user_update'),
    path('auth/me/delete', UserDeleteView.as_view(), name='user_delete'),

    # JWT token management
    path('auth/refresh', RefreshTokenView.as_view(), name='refresh_token'),

    # Telegram authentication
    path('auth/telegram', TelegramAuthView.as_view(), name='telegram_auth'),

    # Phone authentication
    path('auth/phone', PhoneAuthView.as_view(), name='phone_auth'),

    # Provider authentication
    path('provider/signup', ProviderSignupView.as_view(), name='provider_signup'),
    path('provider/list', ProviderListView.as_view(), name='provider_list'),

    # Health check
    path('health', health_check, name='health_check'),
]