"""
Routers for the FastAPI application
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from .models import (
    User, UserCreate, UserUpdate, UserListResponse, 
    PaginationInfo, HealthResponse, SuccessResponse, ErrorResponse
)
from .services import get_user_service, get_system_service, UserService, SystemService
from .config import settings

# Create routers
user_router = APIRouter(prefix="/api/users", tags=["users"])
system_router = APIRouter(tags=["system"])


@user_router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    name="Create User",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User with this email already exists"},
        422: {"description": "Validation error"}
    }
)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Create a new user.
    
    This endpoint creates a new user with the provided information.
    Email must be unique across all users.
    
    Args:
        user_data: User creation data including name, email, age, and status
        user_service: Injected user service for creating users
        
    Returns:
        User: Created user with generated ID and timestamps
        
    Raises:
        HTTPException: If user with this email already exists
    """
    # Check if user already exists
    existing_user = await user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    return await user_service.create_user(user_data)


@user_router.get(
    "/",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
    name="List Users",
    responses={
        200: {"description": "Users retrieved successfully"},
        422: {"description": "Validation error"}
    }
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    user_service: UserService = Depends(get_user_service)
) -> UserListResponse:
    """
    List users with pagination.
    
    This endpoint retrieves a paginated list of users with optional filtering.
    
    Args:
        page: Page number (starts from 1)
        limit: Number of items per page (max 100)
        user_service: Injected user service for retrieving users
        
    Returns:
        UserListResponse: List of users with pagination information
    """
    skip = (page - 1) * limit
    users = await user_service.list_users(skip=skip, limit=limit)
    total = await user_service.count_users()
    
    pagination = PaginationInfo(
        page=page,
        limit=limit,
        total=total,
        pages=(total + limit - 1) // limit
    )
    
    return UserListResponse(users=users, pagination=pagination)


@user_router.get(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    name="Get User",
    responses={
        200: {"description": "User retrieved successfully"},
        404: {"description": "User not found"},
        422: {"description": "Validation error"}
    }
)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Get user by ID.
    
    This endpoint retrieves detailed information about a specific user
    including their profile data and timestamps.
    
    Args:
        user_id: Unique user identifier
        user_service: Injected user service for retrieving user data
        
    Returns:
        User: User details including profile and metadata
        
    Raises:
        HTTPException: If user is not found
    """
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@user_router.put(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    name="Update User",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        422: {"description": "Validation error"}
    }
)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Update user information.
    
    This endpoint updates an existing user's information.
    Only provided fields will be updated.
    
    Args:
        user_id: Unique user identifier
        user_data: User update data (only provided fields will be updated)
        user_service: Injected user service for updating users
        
    Returns:
        User: Updated user details
        
    Raises:
        HTTPException: If user is not found
    """
    # Check if user exists
    existing_user = await user_service.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )
    
    return updated_user


@user_router.delete(
    "/{user_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    name="Delete User",
    responses={
        200: {"description": "User deleted successfully"},
        404: {"description": "User not found"}
    }
)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> SuccessResponse:
    """
    Delete user.
    
    This endpoint permanently deletes a user and all associated data.
    
    Args:
        user_id: Unique user identifier
        user_service: Injected user service for deleting users
        
    Returns:
        SuccessResponse: Confirmation message
        
    Raises:
        HTTPException: If user is not found
    """
    # Check if user exists
    existing_user = await user_service.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
    
    return SuccessResponse(message="User deleted successfully")


@system_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    name="Health Check",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"}
    }
)
async def health_check(
    system_service: SystemService = Depends(get_system_service)
) -> HealthResponse:
    """
    Health check endpoint.
    
    This endpoint checks the health status of the service and its dependencies.
    
    Args:
        system_service: Injected system service for health checks
        
    Returns:
        HealthResponse: Health status information
    """
    health_data = await system_service.health_check()
    
    if health_data["status"] == "healthy":
        return HealthResponse(**health_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unhealthy"
        )
