"""
Authentication module for WDEAF
Handles email/password and phone-based authentication with PostgreSQL
Telegram auth temporarily disabled for initial rollout
"""

import json
import logging
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field, field_validator
from jwt import encode, decode, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from config import BOT_TOKEN, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
from database import get_session
from services.auth_service import AuthServiceDB

logger = logging.getLogger("wdeaf.auth")
router = APIRouter(prefix="/api/auth", tags=["auth"])


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class UserResponseSchema(BaseModel):
    id: int
    telegram_id: Optional[int] = None
    email: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    is_provider: bool = False
    auth_provider: str = "email"

    model_config = {"from_attributes": True}


class AuthResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponseSchema


class EmailLoginRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class EmailSignupRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class PhoneAuthRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+\d{10,15}$")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=32)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v.startswith("+"):
            raise ValueError("Phone must start with +")
        return v


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ============================================================================
# JWT UTILITIES
# ============================================================================

def create_access_token(
    user_id: int,
    expires_hours: Optional[int] = None,
) -> str:
    exp = expires_hours or JWT_EXPIRATION_HOURS
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=exp),
        "iat": datetime.utcnow(),
        "type": "access",
    }
    return encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=30),
        "iat": datetime.utcnow(),
        "type": "refresh",
    }
    return encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except InvalidTokenError as e:
        logger.error(f"❌ Token decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# ============================================================================
# AUTH DEPENDENCY
# ============================================================================

async def get_current_user_dep(
    authorization: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session),
) -> "UserResponseSchema":
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )

    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    user_id = int(payload["sub"])

    svc = AuthServiceDB(session)
    user = await svc.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponseSchema.model_validate(user)


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/signup", response_model=AuthResponseSchema)
async def email_signup(
    request: EmailSignupRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponseSchema:
    """Register new user with email + password"""
    svc = AuthServiceDB(session)

    try:
        user = await svc.register_email_user(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return AuthResponseSchema(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user=UserResponseSchema.model_validate(user),
    )


@router.post("/login", response_model=AuthResponseSchema)
async def email_login(
    request: EmailLoginRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponseSchema:
    """Login with email + password"""
    svc = AuthServiceDB(session)
    user = await svc.authenticate_email_user(request.email, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return AuthResponseSchema(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user=UserResponseSchema.model_validate(user),
    )


@router.post("/phone", response_model=AuthResponseSchema)
async def phone_login(
    request: PhoneAuthRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponseSchema:
    """Login/register via phone number"""
    svc = AuthServiceDB(session)
    user = await svc.find_or_create_phone_user(
        phone=request.phone,
        first_name=request.first_name,
        last_name=request.last_name,
        username=request.username,
    )

    return AuthResponseSchema(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user=UserResponseSchema.model_validate(user),
    )


@router.post("/refresh", response_model=AuthResponseSchema)
async def refresh_token(
    request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponseSchema:
    """Refresh access token using refresh token"""
    payload = decode_token(request.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = int(payload["sub"])
    svc = AuthServiceDB(session)
    user = await svc.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return AuthResponseSchema(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user=UserResponseSchema.model_validate(user),
    )


@router.get("/me", response_model=UserResponseSchema)
async def get_me(
    current_user: UserResponseSchema = Depends(get_current_user_dep),
) -> UserResponseSchema:
    """Get current authenticated user"""
    return current_user
