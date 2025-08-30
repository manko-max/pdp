# Celery Advanced - Complete Guide

## Table of Contents
1. [Queue Management](#queue-management)
2. [Multiple Brokers](#multiple-brokers)
3. [Result Backend Management](#result-backend-management)
4. [Late/Manual Acknowledgement](#latemanual-acknowledgement)
5. [Soft/Hard Timeouts](#softhard-timeouts)
6. [Workflow Design](#workflow-design)
7. [Signatures](#signatures)
8. [Primitives](#primitives)
9. [Stamping](#stamping)
10. [Practical Examples](#practical-examples)

## Queue Management

### Basic Queue Configuration

```python
# settings.py
CELERY_TASK_ROUTES = {
    'app.tasks.send_email': {'queue': 'email'},
    'app.tasks.process_image': {'queue': 'image_processing'},
    'app.tasks.cleanup': {'queue': 'maintenance'},
}

# Priority queues
CELERY_TASK_ROUTES = {
    'app.tasks.urgent_task': {'queue': 'high_priority'},
    'app.tasks.normal_task': {'queue': 'normal_priority'},
    'app.tasks.low_task': {'queue': 'low_priority'},
}
```

### Queue with Parameters

```python
CELERY_TASK_ROUTES = {
    'app.tasks.heavy_task': {
        'queue': 'heavy_processing',
        'routing_key': 'heavy',
        'priority': 9,
    }
}
```

### Starting Workers for Specific Queues

```bash
# Start worker for specific queue
celery -A myapp worker --loglevel=info --queues=email

# Start worker for multiple queues
celery -A myapp worker --loglevel=info --queues=email,image_processing

# Start worker with concurrency
celery -A myapp worker --loglevel=info --queues=heavy_processing --concurrency=2
```

## Multiple Brokers

### Configuration

```python
# celery_config.py
from kombu import Queue

# Main broker (Redis)
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Additional brokers for different tasks
CELERY_TASK_ROUTES = {
    'app.tasks.critical_task': {
        'queue': 'critical',
        'broker': 'redis://localhost:6379/1'  # Separate Redis DB
    },
    'app.tasks.batch_task': {
        'queue': 'batch',
        'broker': 'amqp://localhost:5672'  # RabbitMQ
    }
}

# Define queues
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('email', routing_key='email'),
    Queue('file_processing', routing_key='file_processing'),
    Queue('critical', routing_key='critical'),
)
```

### Multiple Celery Apps

```python
# tasks.py
from celery import Celery

# Main application
app = Celery('myapp')

# Additional applications with different brokers
email_app = Celery('email_worker')
email_app.config_from_object('email_config')

file_app = Celery('file_worker')
file_app.config_from_object('file_config')

@app.task
def process_data(data):
    # Uses main broker
    pass

@email_app.task
def send_email(email_data):
    # Uses email broker
    pass

@file_app.task
def process_file(file_path):
    # Uses file broker
    pass
```

## Result Backend Management

### Configuration

```python
# Main broker for tasks
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Separate broker for results
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

# Or different storage types
CELERY_RESULT_BACKEND = 'database+postgresql://user:pass@localhost/db'
CELERY_RESULT_BACKEND = 'cache+memcached://127.0.0.1:11211/'

# Result settings
CELERY_RESULT_EXPIRES = 3600  # Results stored for 1 hour
CELERY_TASK_RESULT_EXPIRES = 1800  # Task results 30 minutes
CELERY_RESULT_PERSISTENT = True  # Persist results to disk
```

### Working with Results

```python
from celery import Celery
from celery.result import AsyncResult

app = Celery('myapp')

@app.task(bind=True)
def long_running_task(self):
    # Send intermediate results
    self.update_state(
        state='PROGRESS',
        meta={'current': 50, 'total': 100}
    )
    return {'result': 'completed'}

# Getting results
result = long_running_task.delay()
print(result.status)  # PENDING, SUCCESS, FAILURE, etc.
print(result.result)  # Task result
print(result.get())   # Blocking get

# Check status
if result.ready():
    print("Task completed")
else:
    print("Task still running")
```

## Late/Manual Acknowledgement

### Automatic Acknowledgement (Default)

```python
@app.task(acks_late=False)  # Default
def auto_ack_task():
    # Task is acknowledged immediately when received
    pass
```

### Late Acknowledgement

```python
@app.task(acks_late=True)
def late_ack_task():
    # Task is acknowledged only after successful completion
    # If worker crashes, task will be restarted
    pass
```

### Manual Acknowledgement

```python
@app.task(bind=True, acks_late=True)
def manual_ack_task(self):
    try:
        # Do work
        result = do_some_work()
        
        # Manual success acknowledgement
        self.acknowledge()
        return result
        
    except Exception as exc:
        # Manual error acknowledgement
        self.acknowledge()
        raise exc
```

### Worker Configuration

```python
# Global settings
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Important for acks_late

# Worker settings
CELERY_WORKER_CONSUMER = 'kombu.Consumer'
CELERY_WORKER_CONSUMER_ARGS = {
    'prefetch_count': 1,
}
```

## Soft/Hard Timeouts

### Soft Timeout

```python
from celery.exceptions import SoftTimeLimitExceeded

@app.task(soft_time_limit=30)  # 30 seconds
def soft_timeout_task():
    try:
        # Task will receive SoftTimeLimitExceeded after 30 seconds
        time.sleep(60)  # Will be interrupted
    except SoftTimeLimitExceeded:
        # Handle soft timeout
        print("Task was soft killed")
        # Can perform cleanup
        cleanup_resources()
        raise
```

### Hard Timeout

```python
@app.task(time_limit=60)  # 60 seconds
def hard_timeout_task():
    # Task will be forcefully killed after 60 seconds
    # No chance to handle it
    time.sleep(120)  # Will be killed forcefully
```

### Combined Timeouts

```python
@app.task(
    soft_time_limit=30,  # Soft timeout
    time_limit=60        # Hard timeout
)
def combined_timeout_task():
    try:
        # Work for 30 seconds
        for i in range(30):
            time.sleep(1)
            print(f"Working... {i}")
            
        # After 30 seconds - SoftTimeLimitExceeded
        time.sleep(60)  # Will be killed after 60 seconds
        
    except SoftTimeLimitExceeded:
        print("Soft timeout - cleaning up")
        cleanup()
        raise
```

### Global Timeout Settings

```python
# Default settings
CELERY_TASK_SOFT_TIME_LIMIT = 300  # 5 minutes
CELERY_TASK_TIME_LIMIT = 600       # 10 minutes

# Worker settings
CELERY_WORKER_TIMER = 'kombu.asynchronous.timer'
CELERY_WORKER_TIMER_PRECISION = 1.0
```

## Workflow Design

### Understanding Signatures

```python
# Regular task call
result = send_email.delay('user@example.com')

# Create signature (not executed immediately)
email_sig = send_email.s('user@example.com')
# email_sig is a "recipe" for the task, but not executed yet

# Execute signature
result = email_sig.delay()  # Now it's executed
```

## Signatures

### Partials

```python
from celery import signature

# Create signature
task_sig = signature('app.tasks.send_email', args=['user@example.com'])

# Execute later
result = task_sig.delay()

# Or with additional parameters
task_sig = signature('app.tasks.send_email', 
                    args=['user@example.com'],
                    kwargs={'template': 'welcome'})
```

### Callbacks

```python
@app.task
def process_data(data):
    return {'processed': data}

@app.task
def send_notification(result):
    print(f"Processing completed: {result}")

# Chain with callback
process_data.apply_async(
    args=[{'data': 'test'}],
    link=send_notification.s()  # Callback
)
```

### Immutability

```python
# Mutable signature
mutable_sig = signature('app.tasks.send_email', args=['user@example.com'])
mutable_sig.args = ['admin@example.com']  # Can be changed

# Immutable signature
immutable_sig = signature('app.tasks.send_email', 
                         args=['user@example.com'],
                         immutable=True)
# immutable_sig.args = ['admin@example.com']  # Error!
```

## Primitives

### Chains (Sequential Execution)

```python
from celery import chain

# Sequential execution
workflow = chain(
    process_data.s({'data': 'input'}),
    validate_data.s(),
    save_data.s()
)

result = workflow.apply_async()
```

### Groups (Parallel Execution)

```python
from celery import group

# Parallel execution
workflow = group(
    send_email.s('user1@example.com'),
    send_email.s('user2@example.com'),
    send_email.s('user3@example.com')
)

result = workflow.apply_async()
```

### Chords (Group + Callback)

```python
from celery import chord

# Group + callback
workflow = chord(
    group(
        process_file.s('file1.txt'),
        process_file.s('file2.txt'),
        process_file.s('file3.txt')
    ),
    merge_results.s()
)

result = workflow.apply_async()
```

### Chunks

```python
from celery import chunks

# Split into chunks
workflow = chunks(
    process_item.s([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    n=3  # 3 items per chunk
)

result = workflow.apply_async()
```

### Maps & Starmaps

```python
from celery import map, starmap

# Map - apply function to list
workflow = map(process_item.s, [1, 2, 3, 4, 5])
result = workflow.apply_async()

# Starmap - unpack arguments
workflow = starmap(process_with_args.s, [(1, 'a'), (2, 'b'), (3, 'c')])
result = workflow.apply_async()
```

## Stamping

### Canvas Stamping

```python
from celery import signature

# Create signature with metadata
task_sig = signature('app.tasks.send_email', 
                    args=['user@example.com'])

# Add stamps
task_sig.stamp('priority', 'high')
task_sig.stamp('retry', max_retries=3)

result = task_sig.apply_async()
```

### Custom Stamping

```python
@app.task(bind=True)
def custom_stamped_task(self):
    # Get stamps
    stamps = self.request.stamps
    print(f"Priority: {stamps.get('priority')}")
    print(f"Retry count: {stamps.get('retry', {}).get('max_retries')}")
```

### Callback Stamping

```python
# Stamping in callback
workflow = chain(
    process_data.s({'data': 'input'}),
    validate_data.s().stamp('validation', strict=True),
    save_data.s()
)
```

## Practical Examples

### Complete Advanced Workflow

```python
from celery import Celery, chain, group, chord, chunks
from celery.exceptions import SoftTimeLimitExceeded

app = Celery('advanced_workflow')

# Configuration
app.conf.update(
    CELERY_TASK_ACKS_LATE=True,
    CELERY_WORKER_PREFETCH_MULTIPLIER=1,
    CELERY_TASK_SOFT_TIME_LIMIT=300,
    CELERY_TASK_TIME_LIMIT=600,
    CELERY_RESULT_BACKEND='redis://localhost:6379/1',
    CELERY_RESULT_EXPIRES=3600,
)

@app.task(bind=True, acks_late=True, soft_time_limit=30)
def process_file(self, file_path):
    try:
        # Process file
        result = {'file': file_path, 'status': 'processed'}
        return result
    except SoftTimeLimitExceeded:
        self.acknowledge()
        raise

@app.task
def merge_results(results):
    return {'merged': results, 'count': len(results)}

@app.task
def send_notification(result):
    print(f"Workflow completed: {result}")

# Complex workflow
def create_workflow(file_paths):
    # 1. Process files in parallel
    file_processing = group(
        process_file.s(path) for path in file_paths
    )
    
    # 2. Merge results
    merge_step = merge_results.s()
    
    # 3. Notification
    notification = send_notification.s()
    
    # Create chord (group + callback)
    workflow = chord(file_processing, merge_step)
    
    # Add notification
    workflow = chain(workflow, notification)
    
    return workflow

# Usage
file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
workflow = create_workflow(file_paths)
result = workflow.apply_async()
```

### Email Processing System

```python
from celery import Celery, group, chain, chord

app = Celery('email_system')

@app.task
def validate_email(email):
    # Validate email format
    return {'email': email, 'valid': True}

@app.task
def send_email(email_data):
    # Send actual email
    return {'sent': email_data['email']}

@app.task
def log_email_sent(result):
    # Log successful email
    print(f"Email sent: {result}")

@app.task
def send_bulk_emails(email_list):
    # Create workflow for bulk emails
    validation_group = group(
        validate_email.s(email) for email in email_list
    )
    
    # After validation, send emails
    send_workflow = chord(
        validation_group,
        group(
            send_email.s() for _ in email_list
        )
    )
    
    # Add logging
    complete_workflow = chain(
        send_workflow,
        log_email_sent.s()
    )
    
    return complete_workflow.apply_async()

# Usage
emails = ['user1@example.com', 'user2@example.com', 'user3@example.com']
result = send_bulk_emails(emails)
```

## Best Practices

### 1. Queue Management
- Separate critical tasks from regular tasks
- Use priority queues for urgent work
- Monitor queue lengths

### 2. Timeout Handling
- Always use soft timeouts for cleanup
- Set appropriate hard timeouts
- Handle SoftTimeLimitExceeded exceptions

### 3. Result Management
- Use separate result backends for large results
- Set appropriate TTL for results
- Clean up old results regularly

### 4. Workflow Design
- Keep workflows simple and testable
- Use appropriate primitives for the task
- Handle errors gracefully

### 5. Monitoring
- Monitor task execution times
- Set up alerts for failed tasks
- Track queue performance

## Conclusion

Celery Advanced provides powerful tools for building reliable, scalable distributed systems. Key concepts include:

- **Queue Management**: Organize tasks by type and priority
- **Multiple Brokers**: Isolate critical tasks and improve reliability
- **Result Management**: Efficiently store and retrieve task results
- **Acknowledgements**: Control when tasks are considered complete
- **Timeouts**: Protect against hanging tasks
- **Workflows**: Compose complex business processes
- **Signatures**: Create reusable task recipes
- **Primitives**: Build sophisticated execution patterns
- **Stamping**: Add metadata to tasks

These features enable building production-ready distributed systems with Celery.
