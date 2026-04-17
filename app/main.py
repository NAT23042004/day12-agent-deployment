import time
import signal
import logging
import json
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import redis

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget
from utils.mock_llm import ask as llm_ask

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False

# Redis client for stateful conversation history
try:
    r = redis.from_url(settings.redis_url, decode_responses=True)
except Exception:
    r = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info(json.dumps({
        "event": "startup",
        "app": settings.app_name,
        "version": settings.app_version,
    }))
    
    # Check Redis connection
    if r:
        try:
            r.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
    
    _is_ready = True
    yield
    _is_ready = False
    logger.info(json.dumps({"event": "shutdown"}))

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    user_id: str = Field(..., description="Unique ID for the user")
    question: str = Field(..., min_length=1)

class AskResponse(BaseModel):
    answer: str
    model: str
    timestamp: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/ready")
def ready():
    if not _is_ready:
        raise HTTPException(status_code=503, detail="App not ready")
    
    if r:
        try:
            r.ping()
        except Exception:
            raise HTTPException(status_code=503, detail="Redis connection failed")
            
    return {"status": "ready"}

@app.post("/ask", response_model=AskResponse)
async def ask(
    body: AskRequest,
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    # Apply security and limits
    check_rate_limit(body.user_id)
    check_budget(body.user_id)
    
    logger.info(json.dumps({
        "event": "ask_request",
        "user_id": body.user_id,
        "question_len": len(body.question),
    }))
    
    # Get history from Redis
    history_key = f"history:{body.user_id}"
    history = []
    if r:
        history = r.lrange(history_key, -10, -1) # Get last 10 messages
    
    # In a real app, we'd pass history to the LLM
    # For this lab, we'll just log it
    if history:
        logger.debug(f"User history found: {len(history)} messages")
        
    answer = llm_ask(body.question)
    
    # Save to Redis (stateless design)
    if r:
        r.rpush(history_key, f"User: {body.question}")
        r.rpush(history_key, f"Agent: {answer}")
        r.expire(history_key, 3600) # Expire history after 1 hour
        
    return AskResponse(
        answer=answer,
        model=settings.llm_model,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

def handle_sigterm(signum, frame):
    logger.info("Received SIGTERM, shutting down...")

signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
