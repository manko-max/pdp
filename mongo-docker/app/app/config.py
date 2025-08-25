"""
Configuration settings for the FastAPI application
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration using Pydantic Settings."""
    
    # Server
    app_debug: bool = Field(default=False, env="APP_DEBUG", description="Debug mode")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST", description="Application host")
    app_port: int = Field(default=5000, env="APP_PORT", description="Application port")
    
    # Security
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY", description="Application secret key")
    jwt_secret_key: str = Field(default="jwt-secret-key", env="JWT_SECRET_KEY", description="JWT secret key")
    bcrypt_log_rounds: int = Field(default=12, env="BCRYPT_LOG_ROUNDS", description="BCrypt log rounds")
    
    # MongoDB
    mongodb_uri: str = Field(
        default="mongodb://localhost:27017/userdb", 
        env="MONGODB_URI", 
        description="MongoDB connection URI"
    )
    mongodb_max_pool_size: int = Field(default=50, env="MONGODB_MAX_POOL_SIZE", description="MongoDB max pool size")
    mongodb_min_pool_size: int = Field(default=10, env="MONGODB_MIN_POOL_SIZE", description="MongoDB min pool size")
    mongodb_max_idle_time_ms: int = Field(default=30000, env="MONGODB_MAX_IDLE_TIME_MS", description="MongoDB max idle time")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL", description="Logging level")
    log_file: str = Field(default="app.log", env="LOG_FILE", description="Log file path")
    
    # Pagination
    default_page_size: int = Field(default=10, env="DEFAULT_PAGE_SIZE", description="Default page size")
    max_page_size: int = Field(default=100, env="MAX_PAGE_SIZE", description="Maximum page size")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
