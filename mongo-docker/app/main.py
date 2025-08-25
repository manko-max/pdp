"""
Main FastAPI application
"""

import signal
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from .config import settings
from .database import connect_database, disconnect_database
from .routers import user_router, system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting application...")
    try:
        await connect_database()
        print("Application started successfully")
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    print("Shutting down application...")
    await disconnect_database()
    print("Application shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="MongoDB Docker API",
        description="FastAPI application with MongoDB for Docker Compose project",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    

    
    # Include routers
    app.include_router(system_router)
    app.include_router(user_router)
    

    
    return app


# Create application instance
app = create_app()


def handle_sigterm(signum, frame):
    """Handle SIGTERM signal."""
    print("Received SIGTERM, shutting down gracefully...")
    sys.exit(0)


def main():
    """Main application entry point."""
    # Setup signal handlers
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigterm)
    
    # Run application with uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug
    )


if __name__ == '__main__':
    main()
