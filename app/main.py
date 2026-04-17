import time
import signal
import logging
import json
import os
import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import redis
from langchain_core.messages import HumanMessage, AIMessage

from config import settings
from auth import verify_api_key
from rate_limiter import check_rate_limit
from cost_guard import check_budget

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

# Add the directory containing main.py to sys.path to allow importing src
sys.path.append(os.path.dirname(__file__))

# Import the real agent graph
try:
    from src.agent.agent import graph
except ImportError as e:
    logger.error(f"ImportError for agent graph: {e}")
    # Fallback to relative import if running as a package
    try:
        from .src.agent.agent import graph
    except ImportError:
        raise e

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
    
    # Prepare history for the agent
    history_key = f"history:{body.user_id}"
    messages = []
    
    if r:
        # Get last 10 messages from Redis
        raw_history = r.lrange(history_key, -10, -1)
        for msg in raw_history:
            if msg.startswith("User: "):
                messages.append(HumanMessage(content=msg[6:]))
            elif msg.startswith("Agent: "):
                messages.append(AIMessage(content=msg[7:]))
    
    # Add the new question
    messages.append(HumanMessage(content=body.question))
    
    try:
        # Invoke the real agent graph
        result = graph.invoke({"messages": messages})
        
        # Extract the final answer
        final_message = result["messages"][-1]
        answer = final_message.content
        
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
    except Exception as e:
        logger.error(f"Error invoking agent: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing your request: {str(e)}")

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
