from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "My Production Agent"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    agent_api_key: str = "secret-key-123"
    openai_api_key: str = ""
    
    llm_model: str = "mock-gpt-4o"
    
    allowed_origins: List[str] = ["*"]
    
    rate_limit_per_minute: int = 10
    daily_budget_usd: float = 1.0
    
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
