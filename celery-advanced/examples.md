# Celery Advanced - Simple Examples

## Understanding `.s()` - Signatures

### What is `.s()`?

`.s()` creates a **signature** - a "recipe" for a task that can be executed later.

```python
# Regular task execution
result = send_email.delay('user@example.com')

# Create signature (not executed yet)
email_recipe = send_email.s('user@example.com')
# email_recipe is just a "recipe", not executed

# Execute the recipe
result = email_recipe.delay()  # Now it's executed
```

### Why use signatures?

Signatures allow you to:
- Create task "recipes" in advance
- Compose complex workflows
- Pass tasks as parameters

## Timeouts - Simple Explanation

### Soft Timeout (Graceful)

```python
from celery.exceptions import SoftTimeLimitExceeded

@app.task(soft_time_limit=30)  # 30 seconds
def my_task():
    try:
        # Work for 60 seconds
        time.sleep(60)
    except SoftTimeLimitExceeded:
        # Celery says: "Time's up, but you can clean up"
        print("Time expired, cleaning up...")
        cleanup_resources()  # Can clean up
        raise  # Finish the task
```

**What happens:**
- After 30 seconds: Celery sends signal "time's up!"
- Task can finish gracefully and clean up
- Like a polite "please finish soon"

### Hard Timeout (Force Kill)

```python
@app.task(time_limit=60)  # 60 seconds
def my_task():
    # Work for 120 seconds
    time.sleep(120)
    # After 60 seconds: TASK IS KILLED FORCEFULLY
    # No warning, no cleanup possible
```

**What happens:**
- After 60 seconds: Task is KILLED
- No warning, no cleanup
- Like "BAM! You're dead!"

## Partials - Pre-configured Tasks

```python
# Create a "template" task
welcome_email = send_email.s('user@example.com', template='welcome')
# welcome_email is a task with email and template already set

# Execute later
result = welcome_email.delay()

# Or create multiple templates
goodbye_email = send_email.s('user@example.com', template='goodbye')
newsletter_email = send_email.s('user@example.com', template='newsletter')
```

## Callbacks - "When Done, Do This"

```python
@app.task
def process_data(data):
    return f"Processed: {data}"

@app.task
def notify_completion(result):
    print(f"Task completed: {result}")

# Execute task, and when done, call notify_completion
process_data.apply_async(
    args=['some data'],
    link=notify_completion.s()  # This is the callback
)
```

**Flow:**
1. `process_data` runs
2. When `process_data` finishes
3. `notify_completion` runs automatically

## Maps - Apply Function to List

```python
from celery import map

# Apply send_email to each email in list
email_list = ['user1@example.com', 'user2@example.com', 'user3@example.com']
workflow = map(send_email.s, email_list)
result = workflow.apply_async()

# This is equivalent to:
# send_email.delay('user1@example.com')
# send_email.delay('user2@example.com') 
# send_email.delay('user3@example.com')
# But all run in parallel!
```

## Starmaps - Unpack Arguments

```python
from celery import starmap

@app.task
def send_personalized_email(name, email):
    return f"Hello {name}, email sent to {email}"

# List of tuples
user_data = [
    ('John', 'john@example.com'),
    ('Jane', 'jane@example.com'),
    ('Bob', 'bob@example.com')
]

# Starmap unpacks tuples into arguments
workflow = starmap(send_personalized_email.s, user_data)
result = workflow.apply_async()

# This calls:
# send_personalized_email('John', 'john@example.com')
# send_personalized_email('Jane', 'jane@example.com')
# send_personalized_email('Bob', 'bob@example.com')
```

## Stamping - Adding Metadata

```python
# Add "stamps" (metadata) to task
email_task = send_email.s('user@example.com')
email_task.stamp('priority', 'high')        # Stamp: priority = high
email_task.stamp('retry', max_retries=5)    # Stamp: max retries = 5
email_task.stamp('department', 'marketing') # Stamp: department = marketing

# In the task, get the stamps
@app.task(bind=True)
def send_email(self, email):
    stamps = self.request.stamps
    priority = stamps.get('priority', 'normal')
    department = stamps.get('department', 'general')
    
    print(f"Sending email with priority: {priority}")
    print(f"Department: {department}")
```

## Complete Example - Email System

```python
from celery import Celery, group, chain, chord
from celery.exceptions import SoftTimeLimitExceeded

app = Celery('email_system')

# Configuration
app.conf.update(
    CELERY_TASK_ACKS_LATE=True,
    CELERY_TASK_SOFT_TIME_LIMIT=30,
    CELERY_TASK_TIME_LIMIT=60,
)

@app.task(bind=True, acks_late=True, soft_time_limit=30)
def validate_email(self, email):
    try:
        # Simulate email validation
        time.sleep(1)
        return {'email': email, 'valid': True}
    except SoftTimeLimitExceeded:
        print(f"Validation timeout for {email}")
        self.acknowledge()
        raise

@app.task
def send_email(email_data):
    # Simulate sending email
    time.sleep(2)
    return f"Email sent to {email_data['email']}"

@app.task
def log_success(result):
    print(f"SUCCESS: {result}")

@app.task
def log_failure(result):
    print(f"FAILURE: {result}")

def send_bulk_emails(email_list):
    # Step 1: Validate all emails in parallel
    validation_group = group(
        validate_email.s(email) for email in email_list
    )
    
    # Step 2: After validation, send emails
    send_workflow = chord(
        validation_group,  # Wait for all validations
        group(
            send_email.s() for _ in email_list  # Then send all emails
        )
    )
    
    # Step 3: Log success
    complete_workflow = chain(
        send_workflow,
        log_success.s()
    )
    
    return complete_workflow.apply_async()

# Usage
emails = [
    'user1@example.com',
    'user2@example.com', 
    'user3@example.com'
]

result = send_bulk_emails(emails)
print(f"Workflow started: {result.id}")
```

## Queue Management Example

```python
# Different queues for different tasks
CELERY_TASK_ROUTES = {
    'app.tasks.send_email': {'queue': 'email'},
    'app.tasks.process_image': {'queue': 'image_processing'},
    'app.tasks.cleanup': {'queue': 'maintenance'},
}

# Start workers for specific queues
# Terminal 1: Email worker
# celery -A myapp worker --queues=email --concurrency=2

# Terminal 2: Image processing worker  
# celery -A myapp worker --queues=image_processing --concurrency=1

# Terminal 3: Maintenance worker
# celery -A myapp worker --queues=maintenance --concurrency=1
```

## Result Management Example

```python
# Separate result storage
CELERY_BROKER_URL = 'redis://localhost:6379/0'      # For tasks
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'  # For results

@app.task(bind=True)
def long_task(self):
    # Send progress updates
    self.update_state(
        state='PROGRESS',
        meta={'current': 25, 'total': 100}
    )
    
    time.sleep(5)
    
    self.update_state(
        state='PROGRESS', 
        meta={'current': 50, 'total': 100}
    )
    
    time.sleep(5)
    
    self.update_state(
        state='PROGRESS',
        meta={'current': 100, 'total': 100}
    )
    
    return {'status': 'completed'}

# Usage
result = long_task.delay()

# Check progress
while not result.ready():
    print(f"Progress: {result.info}")
    time.sleep(1)

print(f"Final result: {result.result}")
```

## Key Takeaways

1. **`.s()`** = Create task "recipe" (signature)
2. **Soft timeout** = Polite "please finish" (can cleanup)
3. **Hard timeout** = Force kill (no cleanup)
4. **Partials** = Pre-configured tasks
5. **Callbacks** = "When done, do this"
6. **Maps** = Apply function to list
7. **Starmaps** = Unpack tuple arguments
8. **Stamping** = Add metadata to tasks

These concepts allow you to build complex, reliable distributed systems with Celery!
