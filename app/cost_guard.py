import redis
import time
from fastapi import HTTPException
from .config import settings

# Redis client
try:
    r = redis.from_url(settings.redis_url, decode_responses=True)
except Exception:
    r = None

def check_budget(user_id: str, estimated_cost: float = 0.001):
    """
    Check if user has enough budget for the request
    """
    if not r:
        return

    today = time.strftime("%Y-%m-%d")
    key = f"cost:{user_id}:{today}"
    
    current_cost = float(r.get(key) or 0)
    
    if current_cost + estimated_cost > settings.daily_budget_usd:
        raise HTTPException(
            status_code=402,
            detail="Daily budget exhausted",
        )
    
    r.incrbyfloat(key, estimated_cost)
    r.expire(key, 24 * 3600)  # 24 hours
