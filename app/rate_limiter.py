import redis
import time
from fastapi import HTTPException
from .config import settings

# Redis client
try:
    r = redis.from_url(settings.redis_url, decode_responses=True)
except Exception:
    r = None

def check_rate_limit(user_id: str):
    """
    Simple sliding window rate limiter using Redis
    """
    if not r:
        # Fallback if Redis is not available (for local dev)
        return

    now = time.time()
    key = f"rate_limit:{user_id}"
    
    # Remove old timestamps
    r.zremrangebyscore(key, 0, now - 60)
    
    # Count requests in the last minute
    request_count = r.zcard(key)
    
    if request_count >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} requests per minute",
            headers={"Retry-After": "60"},
        )
    
    # Add current request
    r.zadd(key, {str(now): now})
    # Expire the key after 1 minute to save memory
    r.expire(key, 60)
