from django.urls import path
from . import views

urlpatterns = [
    # Auth endpoints
    path('api/auth/signup', views.email_signup, name='email_signup'),
    path('api/auth/login', views.email_login, name='email_login'),
    path('api/auth/phone', views.phone_auth, name='phone_auth'),
    path('api/auth/refresh', views.refresh_token, name='refresh_token'),
    path('api/auth/me', views.get_current_user, name='get_current_user'),
    
    # Health check
    path('health', views.health_check, name='health_check'),
]