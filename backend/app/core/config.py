from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Jal Sathi"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://jalsathi:jalsathi@db:5432/jalsathi"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_CACHE_TTL: int = 21600  # 6 hours
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Weather APIs
    WEATHER_API_KEY: str = ""
    IMD_API_KEY: str = ""
    
    # SMS Gateway
    SMS_GATEWAY_URL: str = ""
    SMS_GATEWAY_API_KEY: str = ""
    
    # Claude AI
    CLAUDE_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
