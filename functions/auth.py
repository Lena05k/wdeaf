"""
Authentication module for WDEAF
Handles Telegram Web Apps validation and phone-based authentication
"""

import logging
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator
from jwt import encode, decode, InvalidTokenError

from config import BOT_TOKEN, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS

logger = logging.getLogger('wdeaf.auth')
router = APIRouter(prefix='/api/auth', tags=['auth'])

# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class UserSchema(BaseModel):
    """User response schema"""
    id: int | str
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True


class AuthResponseSchema(BaseModel):
    """Auth response with token and user"""
    access_token: str
    token_type: str = 'bearer'
    user: UserSchema


class TelegramAuthRequest(BaseModel):
    """Telegram Web App auth request"""
    init_data: str = Field(..., description='Telegram initData string')


class PhoneAuthRequest(BaseModel):
    """Phone authentication request"""
    phone: str = Field(
        ...,
        regex=r'^\+\d{10,15}$',
        description='Phone number in format +7XXXXXXXXXX'
    )
    first_name: str = Field(..., min_length=1, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=32)
    last_name: Optional[str] = Field(None, max_length=100)

    @validator('phone')
    def validate_phone(cls, v: str) -> str:
        """Validate phone number format"""
        if not v.startswith('+'):
            raise ValueError('Phone must start with +')
        if len(v) < 11 or len(v) > 16:
            raise ValueError('Phone length must be between 11 and 16 characters')
        return v

    @validator('username')
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """Validate Telegram username"""
        if v and not v.replace('_', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


# ============================================================================
# JWT UTILITIES
# ============================================================================

def create_access_token(user_id: int | str, expires_hours: Optional[int] = None) -> str:
    """
    Create JWT access token
    
    Args:
        user_id: User ID
        expires_hours: Token expiration time in hours (default: JWT_EXPIRATION_HOURS)
    """
    if expires_hours is None:
        expires_hours = JWT_EXPIRATION_HOURS

    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    payload = {
        'sub': str(user_id),
        'exp': expire,
        'iat': datetime.utcnow(),
        'type': 'access'
    }

    token = encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    logger.info(f'✅ Access token created for user {user_id}')
    return token


def decode_token(token: str) -> dict:
    """
    Decode and validate JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except InvalidTokenError as e:
        logger.error(f'❌ Token decode error: {e}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token'
        )


# ============================================================================
# TELEGRAM VALIDATION
# ============================================================================

def validate_telegram_signature(init_data: str) -> dict:
    """
    Validate Telegram Mini App init data signature
    
    Based on: https://core.telegram.org/bots/webapps#validating-data-received-from-the-mini-app
    
    Args:
        init_data: Raw init data string from Telegram
        
    Returns:
        Parsed init data dict
        
    Raises:
        HTTPException: If signature is invalid
    """
    try:
        # Parse init_data query string
        data_check_string_parts = []
        init_data_pairs = init_data.split('&')
        init_data_dict = {}

        for pair in init_data_pairs:
            if '=' not in pair:
                continue
            
            key, value = pair.split('=', 1)
            init_data_dict[key] = value

            if key != 'hash':
                data_check_string_parts.append(pair)

        # Sort by key and join
        data_check_string_parts.sort()
        data_check_string = '\n'.join(data_check_string_parts)

        # Validate signature
        secret_key = hmac.new(
            b'WebAppData',
            BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()

        received_hash = init_data_dict.get('hash', '')
        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if received_hash != computed_hash:
            logger.warning('❌ Telegram signature validation failed')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Telegram signature'
            )

        logger.info('✅ Telegram signature validated')
        return init_data_dict

    except ValueError as e:
        logger.error(f'❌ Telegram validation error: {e}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid init data format'
        )


# ============================================================================
# USER DATABASE FUNCTIONS (MOCK)
# ============================================================================
# TODO: Replace with actual database calls when DB is set up

# In-memory user storage for development
USERS_DB: dict = {}


def find_or_create_user_telegram(telegram_id: int, user_data: dict) -> dict:
    """
    Find or create user from Telegram data
    
    Args:
        telegram_id: Telegram user ID
        user_data: Telegram user data dict
        
    Returns:
        User dict
    """
    user_id = f'tg_{telegram_id}'
    
    if user_id not in USERS_DB:
        USERS_DB[user_id] = {
            'id': telegram_id,
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name'),
            'username': user_data.get('username'),
            'phone': None,
            'created_at': datetime.utcnow().isoformat()
        }
        logger.info(f'👤 New user created from Telegram: {user_id}')
    else:
        logger.info(f'✅ User found: {user_id}')
    
    return USERS_DB[user_id]


def find_or_create_user_phone(phone: str, user_data: dict) -> dict:
    """
    Find or create user from phone auth
    
    Args:
        phone: Phone number
        user_data: User data dict (first_name, username, etc.)
        
    Returns:
        User dict
    """
    # Use phone as key
    user_id = f'phone_{phone}'
    
    if user_id not in USERS_DB:
        USERS_DB[user_id] = {
            'id': phone,
            'first_name': user_data['first_name'],
            'last_name': user_data.get('last_name'),
            'username': user_data.get('username'),
            'phone': phone,
            'created_at': datetime.utcnow().isoformat()
        }
        logger.info(f'👤 New user created from phone: {user_id}')
    else:
        logger.info(f'✅ User found: {user_id}')
    
    return USERS_DB[user_id]


# ============================================================================
# ROUTES
# ============================================================================

@router.post('/telegram', response_model=AuthResponseSchema)
async def telegram_login(request: TelegramAuthRequest) -> AuthResponseSchema:
    """
    Authenticate user via Telegram Web App
    
    Validates Telegram signature and creates/retrieves user
    
    Args:
        request: TelegramAuthRequest with init_data
        
    Returns:
        AuthResponseSchema with access token and user data
    """
    try:
        # Validate Telegram signature
        init_data = validate_telegram_signature(request.init_data)
        
        # Get user data from init_data
        import json
        from urllib.parse import unquote
        
        user_data_str = init_data.get('user')
        if not user_data_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No user data in Telegram response'
            )
        
        # Decode user JSON
        user_data = json.loads(unquote(user_data_str))
        telegram_id = user_data.get('id')
        
        if not telegram_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No user ID in Telegram response'
            )
        
        # Find or create user
        user = find_or_create_user_telegram(telegram_id, user_data)
        
        # Create token
        access_token = create_access_token(user['id'])
        
        return AuthResponseSchema(
            access_token=access_token,
            token_type='bearer',
            user=UserSchema(**user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'❌ Telegram login error: {e}', exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Authentication error'
        )


@router.post('/phone', response_model=AuthResponseSchema)
async def phone_login(request: PhoneAuthRequest) -> AuthResponseSchema:
    """
    Authenticate user via phone number
    
    Args:
        request: PhoneAuthRequest with phone, first_name, and optional username
        
    Returns:
        AuthResponseSchema with access token and user data
    """
    try:
        # Find or create user
        user = find_or_create_user_phone(
            request.phone,
            {
                'first_name': request.first_name,
                'last_name': request.last_name,
                'username': request.username
            }
        )
        
        # Create token
        access_token = create_access_token(user['id'])
        
        return AuthResponseSchema(
            access_token=access_token,
            token_type='bearer',
            user=UserSchema(**user)
        )
        
    except Exception as e:
        logger.error(f'❌ Phone login error: {e}', exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Authentication error'
        )


@router.post('/refresh', response_model=AuthResponseSchema)
async def refresh_token(request: RefreshTokenRequest) -> AuthResponseSchema:
    """
    Refresh access token
    
    Args:
        request: RefreshTokenRequest with refresh_token
        
    Returns:
        New access token
    """
    try:
        # Decode refresh token
        payload = decode_token(request.refresh_token)
        
        if payload.get('type') != 'refresh':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type'
            )
        
        user_id = payload.get('sub')
        
        # Create new access token
        access_token = create_access_token(user_id, expires_hours=1)
        
        return AuthResponseSchema(
            access_token=access_token,
            token_type='bearer',
            user=UserSchema(id=user_id, first_name='User')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'❌ Token refresh error: {e}', exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Token refresh failed'
        )


@router.get('/me')
async def get_current_user(token: str = None) -> UserSchema:
    """
    Get current authenticated user
    
    Args:
        token: Authorization token from header
        
    Returns:
        Current user data
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No token provided'
        )
    
    try:
        payload = decode_token(token)
        user_id = payload.get('sub')
        
        # Find user in DB
        for db_user in USERS_DB.values():
            if str(db_user['id']) == str(user_id):
                return UserSchema(**db_user)
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f'❌ Get user error: {e}', exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error retrieving user'
        )
