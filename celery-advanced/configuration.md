# Celery Advanced Configuration

## Complete Configuration Example

```python
# celery_config.py
from kombu import Queue
from celery import Celery

# Create Celery app
app = Celery('advanced_app')

# Basic configuration
app.conf.update(
    # Broker settings
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/1',
    
    # Task settings
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE='UTC',
    CELERY_ENABLE_UTC=True,
    
    # Worker settings
    CELERY_WORKER_PREFETCH_MULTIPLIER=1,
    CELERY_TASK_ACKS_LATE=True,
    CELERY_WORKER_DISABLE_RATE_LIMITS=False,
    
    # Timeout settings
    CELERY_TASK_SOFT_TIME_LIMIT=300,  # 5 minutes
    CELERY_TASK_TIME_LIMIT=600,       # 10 minutes
    
    # Result settings
    CELERY_RESULT_EXPIRES=3600,       # 1 hour
    CELERY_TASK_RESULT_EXPIRES=1800,  # 30 minutes
    CELERY_RESULT_PERSISTENT=True,
    
    # Retry settings
    CELERY_TASK_DEFAULT_RETRY_DELAY=60,
    CELERY_TASK_MAX_RETRIES=3,
    
    # Queue settings
    CELERY_TASK_DEFAULT_QUEUE='default',
    CELERY_TASK_DEFAULT_EXCHANGE='default',
    CELERY_TASK_DEFAULT_ROUTING_KEY='default',
)

# Define queues
CELERY_TASK_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('email', routing_key='email'),
    Queue('image_processing', routing_key='image_processing'),
    Queue('file_processing', routing_key='file_processing'),
    Queue('maintenance', routing_key='maintenance'),
    Queue('high_priority', routing_key='high_priority'),
    Queue('low_priority', routing_key='low_priority'),
)

# Task routing
CELERY_TASK_ROUTES = {
    'app.tasks.send_email': {'queue': 'email'},
    'app.tasks.process_image': {'queue': 'image_processing'},
    'app.tasks.process_file': {'queue': 'file_processing'},
    'app.tasks.cleanup': {'queue': 'maintenance'},
    'app.tasks.urgent_task': {'queue': 'high_priority'},
    'app.tasks.background_task': {'queue': 'low_priority'},
}

# Multiple broker configuration
CELERY_TASK_ROUTES.update({
    'app.tasks.critical_task': {
        'queue': 'critical',
        'broker': 'redis://localhost:6379/2'
    },
    'app.tasks.batch_task': {
        'queue': 'batch',
        'broker': 'amqp://localhost:5672'
    }
})

# Worker configuration
CELERY_WORKER_CONSUMER = 'kombu.Consumer'
CELERY_WORKER_CONSUMER_ARGS = {
    'prefetch_count': 1,
}

# Monitoring
CELERY_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

# Security
CELERY_TASK_ANNOTATIONS = {
    '*': {
        'rate_limit': '100/m',  # 100 tasks per minute
    },
    'app.tasks.send_email': {
        'rate_limit': '10/m',   # 10 emails per minute
    }
}
```

## Environment-based Configuration

```python
# config.py
import os
from kombu import Queue

class Config:
    # Basic settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
    
    # Task settings
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
    
    # Worker settings
    CELERY_WORKER_PREFETCH_MULTIPLIER = int(os.getenv('CELERY_PREFETCH_MULTIPLIER', '1'))
    CELERY_TASK_ACKS_LATE = os.getenv('CELERY_ACKS_LATE', 'True').lower() == 'true'
    
    # Timeout settings
    CELERY_TASK_SOFT_TIME_LIMIT = int(os.getenv('CELERY_SOFT_TIME_LIMIT', '300'))
    CELERY_TASK_TIME_LIMIT = int(os.getenv('CELERY_TIME_LIMIT', '600'))
    
    # Result settings
    CELERY_RESULT_EXPIRES = int(os.getenv('CELERY_RESULT_EXPIRES', '3600'))
    CELERY_TASK_RESULT_EXPIRES = int(os.getenv('CELERY_TASK_RESULT_EXPIRES', '1800'))
    
    # Queue configuration
    CELERY_TASK_QUEUES = (
        Queue('default', routing_key='default'),
        Queue('email', routing_key='email'),
        Queue('processing', routing_key='processing'),
        Queue('maintenance', routing_key='maintenance'),
    )
    
    # Task routing
    CELERY_TASK_ROUTES = {
        'app.tasks.send_email': {'queue': 'email'},
        'app.tasks.process_data': {'queue': 'processing'},
        'app.tasks.cleanup': {'queue': 'maintenance'},
    }

class DevelopmentConfig(Config):
    CELERY_TASK_ALWAYS_EAGER = True  # Execute tasks synchronously
    CELERY_TASK_EAGER_PROPAGATES = True

class ProductionConfig(Config):
    CELERY_TASK_ALWAYS_EAGER = False
    CELERY_WORKER_CONCURRENCY = int(os.getenv('CELERY_CONCURRENCY', '4'))
    CELERY_WORKER_MAX_TASKS_PER_CHILD = int(os.getenv('CELERY_MAX_TASKS_PER_CHILD', '1000'))

class TestingConfig(Config):
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = 'memory://'
    CELERY_RESULT_BACKEND = 'cache+memory://'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

## Docker Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  celery-worker:
    build: .
    command: celery -A app.celery worker --loglevel=info --queues=default,email,processing
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis
    volumes:
      - .:/app

  celery-worker-email:
    build: .
    command: celery -A app.celery worker --loglevel=info --queues=email --concurrency=2
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis
    volumes:
      - .:/app

  celery-worker-processing:
    build: .
    command: celery -A app.celery worker --loglevel=info --queues=processing --concurrency=1
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis
    volumes:
      - .:/app

  celery-beat:
    build: .
    command: celery -A app.celery beat --loglevel=info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis
    volumes:
      - .:/app

  celery-flower:
    build: .
    command: celery -A app.celery flower --port=5555
    ports:
      - "5555:5555"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
    depends_on:
      - redis

volumes:
  redis_data:
```

## Monitoring Configuration

```python
# monitoring.py
from celery import Celery
from celery.signals import task_prerun, task_postrun, task_failure

app = Celery('monitored_app')

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    print(f"Task {task.name} started with ID {task_id}")

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **kwds):
    print(f"Task {task.name} finished with state {state}")

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    print(f"Task {sender.name} failed: {exception}")

# Enable monitoring
app.conf.update(
    CELERY_SEND_TASK_EVENTS=True,
    CELERY_TASK_SEND_SENT_EVENT=True,
    CELERY_WORKER_SEND_TASK_EVENTS=True,
)
```

## Security Configuration

```python
# security.py
from celery import Celery

app = Celery('secure_app')

# Rate limiting
CELERY_TASK_ANNOTATIONS = {
    '*': {
        'rate_limit': '100/m',  # 100 tasks per minute globally
    },
    'app.tasks.send_email': {
        'rate_limit': '10/m',   # 10 emails per minute
    },
    'app.tasks.process_file': {
        'rate_limit': '5/m',    # 5 files per minute
    }
}

# Task time limits
CELERY_TASK_ANNOTATIONS.update({
    'app.tasks.long_running_task': {
        'time_limit': 1800,     # 30 minutes
        'soft_time_limit': 1500, # 25 minutes
    }
})

# Retry configuration
CELERY_TASK_ANNOTATIONS.update({
    'app.tasks.network_task': {
        'default_retry_delay': 60,
        'max_retries': 3,
    }
})

app.conf.update(
    CELERY_TASK_ANNOTATIONS=CELERY_TASK_ANNOTATIONS,
    
    # Security settings
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    
    # Disable pickle for security
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
)
```

## Performance Tuning

```python
# performance.py
from celery import Celery

app = Celery('performance_app')

# Worker optimization
app.conf.update(
    # Prefetch settings
    CELERY_WORKER_PREFETCH_MULTIPLIER=1,
    CELERY_TASK_ACKS_LATE=True,
    
    # Concurrency settings
    CELERY_WORKER_CONCURRENCY=4,
    CELERY_WORKER_MAX_TASKS_PER_CHILD=1000,
    
    # Memory optimization
    CELERY_WORKER_MAX_MEMORY_PER_CHILD=200000,  # 200MB
    
    # Connection pooling
    CELERY_BROKER_POOL_LIMIT=10,
    CELERY_BROKER_CONNECTION_RETRY=True,
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True,
    
    # Result backend optimization
    CELERY_RESULT_BACKEND_MAX_RETRIES=10,
    CELERY_RESULT_BACKEND_RETRY_DELAY=0.1,
    
    # Task optimization
    CELERY_TASK_COMPRESSION='gzip',
    CELERY_RESULT_COMPRESSION='gzip',
    
    # Serialization optimization
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
)
```

## Best Practices

### 1. Configuration Management
- Use environment variables for sensitive data
- Separate configurations for different environments
- Use configuration classes for organization

### 2. Queue Management
- Separate critical tasks from regular tasks
- Use priority queues for urgent work
- Monitor queue lengths and performance

### 3. Worker Management
- Use appropriate concurrency levels
- Set memory limits to prevent memory leaks
- Restart workers periodically

### 4. Monitoring
- Enable task events for monitoring
- Use Flower for web-based monitoring
- Set up alerts for failed tasks

### 5. Security
- Use JSON serialization (disable pickle)
- Implement rate limiting
- Use appropriate timeouts
- Validate task inputs

### 6. Performance
- Tune prefetch settings
- Use connection pooling
- Compress large results
- Monitor resource usage
