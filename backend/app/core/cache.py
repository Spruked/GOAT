# backend/app/core/cache.py
"""
Redis cache management
"""

import redis.asyncio as redis
from app.config import settings

redis_client = None

async def init_cache():
    """Initialize Redis connection"""
    global redis_client

    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )

        # Test connection
        await redis_client.ping()

    except Exception as e:
        print(f"Warning: Redis not available: {e}. Running without cache.")
        redis_client = None

async def get_cache_status() -> bool:
    """Check Redis connectivity"""
    try:
        await redis_client.ping()
        return True
    except:
        return False