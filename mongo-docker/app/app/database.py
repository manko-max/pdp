"""
Database connections and utilities for FastAPI
"""

import asyncio
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings
import structlog

logger = structlog.get_logger()


class Database:
    """Database connection manager."""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(
                settings.mongodb_uri,
                maxPoolSize=settings.mongodb_max_pool_size,
                minPoolSize=settings.mongodb_min_pool_size,
                maxIdleTimeMS=settings.mongodb_max_idle_time_ms
            )
            self.db = self.client.get_database()
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB")
            
            # Create indexes
            await self._create_indexes()
            
        except Exception as e:
            logger.error("Failed to connect to MongoDB", error=str(e))
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create database indexes."""
        try:
            # Users collection indexes
            await self.db.users.create_index("email", unique=True)
            await self.db.users.create_index("created_at", -1)
            await self.db.users.create_index([("status", 1), ("created_at", -1)])
            
            # Sessions collection indexes
            await self.db.sessions.create_index("session_id", unique=True)
            await self.db.sessions.create_index("user_id", 1)
            await self.db.sessions.create_index("expires_at", 1)
            
            logger.info("Database indexes created")
        except Exception as e:
            logger.warning("Failed to create indexes", error=str(e))


# Global database instance
database = Database()


async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance for dependency injection."""
    if database.db is None:
        await database.connect()
    return database.db


async def connect_database():
    """Connect to database on startup."""
    await database.connect()


async def disconnect_database():
    """Disconnect from database on shutdown."""
    await database.disconnect()
