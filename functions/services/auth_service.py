"""
Auth service — business logic layer
All DB interactions go through this service
"""

import logging
from typing import Optional

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User

logger = logging.getLogger("wdeaf.auth_service")


class AuthServiceDB:
    """Database-backed authentication service"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ─── Password hashing ───────────────────────────────────────────

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed.encode("utf-8"),
        )

    # ─── Telegram auth ──────────────────────────────────────────────

    async def find_or_create_telegram_user(
        self,
        telegram_id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            await self.session.commit()
            await self.session.refresh(user)
            logger.info(f"✅ Telegram user updated: {telegram_id}")
            return user

        user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            auth_provider="telegram",
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"👤 New Telegram user created: {telegram_id}")
        return user

    # ─── Email registration ─────────────────────────────────────────

    async def register_email_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: Optional[str] = None,
    ) -> User:
        exists = await self.session.execute(
            select(User).where(User.email == email)
        )
        if exists.scalar_one_or_none():
            raise ValueError("Email already registered")

        user = User(
            email=email,
            password_hash=self.hash_password(password),
            first_name=first_name,
            last_name=last_name,
            auth_provider="email",
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"👤 New email user registered: {email}")
        return user

    # ─── Email login ─────────────────────────────────────────────────

    async def authenticate_email_user(
        self,
        email: str,
        password: str,
    ) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user or not user.password_hash:
            return None

        if not self.verify_password(password, user.password_hash):
            return None

        return user

    # ─── Phone auth ──────────────────────────────────────────────────

    async def find_or_create_phone_user(
        self,
        phone: str,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        result = await self.session.execute(
            select(User).where(User.phone == phone)
        )
        user = result.scalar_one_or_none()

        if user:
            return user

        user = User(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            username=username,
            auth_provider="phone",
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"👤 New phone user created: {phone}")
        return user

    # ─── Get by ID ───────────────────────────────────────────────────

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
