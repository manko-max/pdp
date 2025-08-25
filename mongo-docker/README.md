# MongoDB Docker Project

## Project Overview

A multi-container Docker application featuring:
- **Web Application**: FastAPI API for user management with automatic Swagger documentation
- **MongoDB Database**: Document database with Motor async driver
- **MongoDB Express**: Web-based admin interface for MongoDB
- **Redis Cache**: Async Redis cache for session management

## Architecture

### FastAPI Design
- **FastAPI** for modern, fast web framework with automatic API documentation
- **Motor** async MongoDB driver instead of PyMongo
- **Redis async** client for non-blocking cache operations
- **Structured logging** with structlog
- **Dependency injection** for clean architecture
- **Pydantic models** for data validation and serialization

### Module Structure
```
app/
├── __init__.py          # Package initialization
├── config.py           # Configuration management with Pydantic Settings
├── database.py         # Database connections and dependency injection
├── models.py           # Pydantic models for data validation
├── services.py         # Business logic services with dependency injection
├── routers.py          # FastAPI routers with proper documentation
├── middleware.py       # Custom middleware for logging and error handling
└── main.py            # Application entry point with lifespan management
```

## Directory Structure

```
mongo-docker/
├── docker-compose.yml
├── env.example
├── .gitignore
├── README.md
├── justfile
├── app/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── app/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── models.py
│       ├── services.py
│       ├── routers.py
│       ├── middleware.py
│       └── main.py
├── scripts/
│   ├── backup.sh
│   └── restore.sh
└── data/
    ├── mongodb/
    └── redis/
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git for version control
- just (optional, for convenience commands)

### Setup Instructions

1. **Clone and Navigate**
```bash
git clone <repository-url>
cd mongo-docker
```

2. **Quick Setup (Recommended)**
```bash
just dev
```

**Or Manual Setup:**

2. **Environment Configuration**
```bash
cp env.example .env
# Edit .env with your configuration
```

3. **Build and Start Services**
```bash
docker-compose up -d
```

4. **Verify Services**
```bash
docker-compose ps
```

5. **Access Applications**
- Web API: http://localhost:5000
- Swagger Documentation: http://localhost:5000/docs
- ReDoc Documentation: http://localhost:5000/redoc
- MongoDB Express: http://localhost:8081
- Health Check: http://localhost:5000/health

## API Documentation

### Automatic Documentation
FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **OpenAPI JSON**: http://localhost:5000/openapi.json

### Example API Usage

**Create User:**
```bash
curl -X POST "http://localhost:5000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "status": "active"
  }'
```

**List Users:**
```bash
curl -X GET "http://localhost:5000/api/users/?page=1&limit=10"
```

**Get User by ID:**
```bash
curl -X GET "http://localhost:5000/api/users/{user_id}"
```

**Update User:**
```bash
curl -X PUT "http://localhost:5000/api/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "age": 31
  }'
```

**Delete User:**
```bash
curl -X DELETE "http://localhost:5000/api/users/{user_id}"
```

## Development Tools

### Just Commands
The project includes a `justfile` with common development tasks:

```bash
# Show all available commands
just

# Development workflow
just dev          # Setup and start development environment
just prod         # Start production-like environment

# Docker management
just build        # Build Docker images
just up           # Start services
just down         # Stop services
just restart      # Restart services
just logs         # Show logs
just clean        # Clean up Docker resources

# Database operations
just backup       # Create MongoDB backup
just restore BACKUP_PATH=path  # Restore from backup

# Code quality
just format       # Format code with Black
just lint         # Run linting with Flake8
just type-check   # Run type checking with MyPy
just test         # Run tests

# Monitoring
just status       # Show service status and resource usage
just health       # Check service health
```

## Poetry Configuration

### Dependency Management
The project uses Poetry for Python dependency management with the following features:

**Main Dependencies:**
- fastapi 0.104+ for modern web framework
- uvicorn for ASGI server
- motor 3.3+ for async MongoDB driver
- redis 5.0+ with hiredis for async caching
- pydantic 2.5+ for data validation
- pydantic-settings for configuration management
- structlog for structured logging
- python-dotenv for environment management

**Development Dependencies:**
- httpx for async HTTP testing
- pytest-asyncio for async test support
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

**Poetry Commands:**
```bash
# Install dependencies
poetry install

# Add new dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name

# Run application
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest

# Format code
poetry run black .

# Type checking
poetry run mypy .
```

## FastAPI Architecture

### Why FastAPI?

**Performance Benefits:**
- **High performance**: One of the fastest Python frameworks available
- **Automatic documentation**: Swagger/OpenAPI docs out of the box
- **Type hints**: Full type checking and validation
- **Modern Python**: Built for Python 3.6+ with async/await
- **Easy to use**: Intuitive API design

**Key Features:**
- **Automatic API documentation** with Swagger UI and ReDoc
- **Data validation** with Pydantic models
- **Dependency injection** for clean architecture
- **Async support** with uvicorn ASGI server
- **Type checking** with full IDE support

### Code Examples

**Pydantic Models:**
```python
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., description="User's email address")
    age: Optional[int] = Field(None, ge=0, le=150)
    status: str = Field(default="active", pattern="^(active|inactive|suspended)$")
```

**Dependency Injection:**
```python
async def get_user_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserService:
    return UserService(db)

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> User:
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**Router with Documentation:**
```python
@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    name="Create User",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User with this email already exists"}
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
    """
    return await user_service.create_user(user_data)
```

## Docker Compose Configuration

### Key Features Implemented

**Networks:**
- Custom network for service communication
- Isolated network for security

**Volumes:**
- Persistent data storage for MongoDB
- Redis data persistence
- Application logs

**Environment Variables:**
- Centralized configuration
- Service-specific settings
- Security credentials

**Dependencies:**
- Service startup ordering
- Health checks
- Restart policies

## Security Configuration

### Authentication
```yaml
# docker-compose.yml
mongodb:
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: secure_password
    MONGO_INITDB_DATABASE: userdb
```

### Network Security
```yaml
# docker-compose.yml
networks:
  app-network:
    driver: bridge
    internal: true  # No external access
```

### Environment Variables
```bash
# .env
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=secure_password
MONGO_DATABASE=userdb
REDIS_PASSWORD=redis_password
SECRET_KEY=your_secret_key
```

## Best Practices

### FastAPI Best Practices
- Use Pydantic models for data validation
- Implement dependency injection
- Use proper HTTP status codes
- Add comprehensive API documentation
- Implement proper error handling

### Docker Best Practices
- Use specific image versions
- Implement health checks
- Use multi-stage builds
- Optimize layer caching
- Security scanning

### Poetry Best Practices
- Use `pyproject.toml` for dependency management
- Lock dependencies with `poetry.lock`
- Use virtual environments
- Specify Python version constraints
- Use dependency groups for dev tools

### Async Best Practices
- Use async/await consistently
- Avoid blocking operations in async code
- Implement proper error handling
- Use connection pooling
- Monitor async performance

### MongoDB Best Practices
- Create appropriate indexes
- Use connection pooling
- Implement proper error handling
- Regular backups
- Monitor performance

### Application Best Practices
- Validate input data with Pydantic
- Implement proper logging
- Use environment variables
- Handle errors gracefully
- Implement caching strategies
