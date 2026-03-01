"""
Token blacklist service using Redis
Similar to MarsStationBackend implementation
"""
import redis
from django.conf import settings
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def get_redis_client():
    """Get Redis client from settings"""
    redis_config = getattr(settings, 'REDIS', {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None
    })
    
    try:
        client = redis.Redis(
            host=redis_config.get('host', 'localhost'),
            port=redis_config.get('port', 6379),
            db=redis_config.get('db', 0),
            password=redis_config.get('password'),
            decode_responses=True
        )
        # Test connection
        client.ping()
        return client
    except redis.ConnectionError as e:
        logger.warning(f"Redis connection failed: {e}")
        return None


def add_token_to_blacklist(token: str, expires_at: datetime) -> Tuple[Optional[str], bool]:
    """
    Add token to blacklist in Redis
    
    Args:
        token: JWT token string
        expires_at: Token expiration time
        
    Returns:
        Tuple of (error_message, success)
    """
    client = get_redis_client()
    
    if client is None:
        # Redis not available, log warning but don't fail
        logger.warning("Redis not available, token will not be blacklisted")
        return None, True
    
    try:
        # Calculate TTL in seconds
        ttl = int((expires_at - datetime.utcnow()).total_seconds())
        if ttl <= 0:
            ttl = 3600  # Default 1 hour if token already expired
        
        # Add to blacklist with TTL
        blacklist_key = f"token_blacklist:{token}"
        client.setex(blacklist_key, ttl, "blacklisted")
        
        logger.info(f"Token added to blacklist, TTL: {ttl}s")
        return None, True
    except Exception as e:
        logger.error(f"Error adding token to blacklist: {e}")
        return str(e), False


def is_token_blacklisted(token: str) -> bool:
    """
    Check if token is in blacklist
    
    Args:
        token: JWT token string
        
    Returns:
        True if token is blacklisted, False otherwise
    """
    client = get_redis_client()
    
    if client is None:
        # Redis not available, assume token is valid
        return False
    
    try:
        blacklist_key = f"token_blacklist:{token}"
        return client.exists(blacklist_key)
    except Exception as e:
        logger.error(f"Error checking token blacklist: {e}")
        return False


def remove_token_from_blacklist(token: str) -> Tuple[Optional[str], bool]:
    """
    Remove token from blacklist
    
    Args:
        token: JWT token string
        
    Returns:
        Tuple of (error_message, success)
    """
    client = get_redis_client()
    
    if client is None:
        return None, True
    
    try:
        blacklist_key = f"token_blacklist:{token}"
        client.delete(blacklist_key)
        return None, True
    except Exception as e:
        logger.error(f"Error removing token from blacklist: {e}")
        return str(e), False
