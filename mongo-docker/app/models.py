"""
Pydantic models for the FastAPI application
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user model."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    status: str = Field(default="active", pattern="^(active|inactive|suspended)$", description="User's status")


class UserCreate(UserBase):
    """Model for creating a new user."""
    pass


class UserUpdate(BaseModel):
    """Model for updating a user."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150, description="User's age")
    status: Optional[str] = Field(None, pattern="^(active|inactive|suspended)$", description="User's status")


class User(UserBase):
    """Complete user model with database fields."""
    id: str = Field(..., alias="_id", description="User's unique identifier")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class PaginationInfo(BaseModel):
    """Pagination information."""
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")


class UserListResponse(BaseModel):
    """Response model for user list with pagination."""
    users: List[User] = Field(..., description="List of users")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    database: str = Field(..., description="Database connection status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")


class SuccessResponse(BaseModel):
    """Success response model."""
    message: str = Field(..., description="Success message")
