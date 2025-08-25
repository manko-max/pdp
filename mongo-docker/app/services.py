"""
Services for the FastAPI application
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Annotated
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from fastapi import Depends

from .models import UserCreate, UserUpdate, User, PaginationInfo
from .database import get_database


class UserService:
    """Service for user operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        user_dict = user_data.model_dump()
        user_dict.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        
        print(f"User created: {user_dict['_id']}, email: {user_dict['email']}")
        return User(**user_dict)
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
                return User(**user)
            return None
        except Exception:
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        user = await self.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
            return User(**user)
        return None
    
    async def update_user(self, user_id: str, update_data: UserUpdate) -> Optional[User]:
        """Update user."""
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return await self.get_user_by_id(user_id)
        
        update_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )
        
        if result.modified_count:
            print(f"User updated: {user_id}")
            return await self.get_user_by_id(user_id)
        return None
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user."""
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            print(f"User deleted: {user_id}")
            return True
        return False
    
    async def list_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """List users with pagination."""
        cursor = self.collection.find().skip(skip).limit(limit)
        users = []
        async for user in cursor:
            user["_id"] = str(user["_id"])
            users.append(User(**user))
        return users
    
    async def count_users(self) -> int:
        """Count total users."""
        return await self.collection.count_documents({})


class SystemService:
    """Service for system operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def health_check(self) -> Dict[str, str]:
        """Perform health check."""
        try:
            await self.db.command('ping')
            return {
                "status": "healthy",
                "database": "connected"
            }
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "database": "disconnected"
            }


# Dependency functions
async def get_user_service(db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]) -> UserService:
    """Get user service instance."""
    return UserService(db)


async def get_system_service(db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]) -> SystemService:
    """Get system service instance."""
    return SystemService(db)
