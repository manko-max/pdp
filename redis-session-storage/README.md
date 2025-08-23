# Redis for Session Storage

## 1. Why Redis is often used for session storage in web applications?

- **Speed**: In-memory storage provides sub-millisecond access times
- **Data Structures**: Built-in support for strings, hashes, lists, sets
- **TTL Support**: Automatic expiration with configurable time-to-live
- **Atomic Operations**: Guaranteed consistency for concurrent access
- **Persistence Options**: Can persist to disk while maintaining speed
- **Horizontal Scaling**: Redis Cluster for distributed sessions
- **Memory Efficiency**: Optimized for high-performance data storage

## 2. How to store and retrieve session data in Redis using Python/Node.js?

### Python Example
```python
import redis
import json
import uuid

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Store session data
def store_session(user_id, session_data):
    session_id = str(uuid.uuid4())
    session_key = f"session:{session_id}"
    
    # Store as JSON with TTL (30 minutes)
    r.setex(session_key, 1800, json.dumps({
        'user_id': user_id,
        'data': session_data,
        'created_at': time.time()
    }))
    
    return session_id

# Retrieve session data
def get_session(session_id):
    session_key = f"session:{session_id}"
    session_data = r.get(session_key)
    
    if session_data:
        return json.loads(session_data)
    return None

# Usage
session_id = store_session(123, {'cart': ['item1', 'item2'], 'theme': 'dark'})
session = get_session(session_id)
```

### Node.js Example
```javascript
const redis = require('redis');
const { v4: uuidv4 } = require('uuid');

const client = redis.createClient();

// Store session data
async function storeSession(userId, sessionData) {
    const sessionId = uuidv4();
    const sessionKey = `session:${sessionId}`;
    
    const session = {
        userId,
        data: sessionData,
        createdAt: Date.now()
    };
    
    // Store with 30-minute TTL
    await client.setEx(sessionKey, 1800, JSON.stringify(session));
    return sessionId;
}

// Retrieve session data
async function getSession(sessionId) {
    const sessionKey = `session:${sessionId}`;
    const sessionData = await client.get(sessionKey);
    
    return sessionData ? JSON.parse(sessionData) : null;
}
```

## 3. How does Redis handle expiration of session data?

```python
# Automatic expiration with TTL
r.setex("session:123", 1800, session_data)  # Expires in 30 minutes

# Manual expiration check
def check_session_expiry(session_id):
    ttl = r.ttl(f"session:{session_id}")
    if ttl == -1:  # No expiration set
        return "No expiration"
    elif ttl == -2:  # Key doesn't exist
        return "Expired"
    else:
        return f"Expires in {ttl} seconds"

# Extend session TTL
def extend_session(session_id, additional_seconds=1800):
    r.expire(f"session:{session_id}", additional_seconds)
```

## 4. Advantages and disadvantages of Redis vs other methods

### Redis Advantages
- **Performance**: 10-100x faster than database storage
- **Memory Efficiency**: Optimized data structures
- **TTL Support**: Built-in automatic expiration
- **Scalability**: Horizontal scaling with Redis Cluster
- **Atomic Operations**: Thread-safe concurrent access

### Redis Disadvantages
- **Memory Cost**: All data stored in RAM
- **Data Loss Risk**: Memory-only storage (unless persistence enabled)
- **Complexity**: Additional infrastructure component
- **Network Latency**: Remote Redis calls vs local cookies

### Comparison Table
| Method | Speed | Persistence | Scalability | Memory Usage |
|--------|-------|-------------|-------------|--------------|
| Redis | Very Fast | Configurable | High | High |
| Database | Slow | Full | Medium | Low |
| Cookies | Fast | None | Low | Very Low |

## 5. Security and privacy when storing session data in Redis

```python
# Secure Redis configuration
redis_config = {
    'host': 'localhost',
    'port': 6379,
    'password': 'strong_password',  # Authentication
    'ssl': True,                    # Encrypted connection
    'ssl_cert_reqs': 'required',
    'decode_responses': True
}

# Encrypt sensitive session data
import cryptography.fernet

def encrypt_session_data(data, key):
    f = cryptography.fernet.Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_session_data(encrypted_data, key):
    f = cryptography.fernet.Fernet(key)
    return json.loads(f.decrypt(encrypted_data).decode())

# Store encrypted session
encrypted_data = encrypt_session_data(session_data, encryption_key)
r.setex(f"session:{session_id}", 1800, encrypted_data)
```

## 6. Redis crash/restart impact and mitigation

### Impact
- **Memory-only Redis**: All session data lost
- **RDB Persistence**: Data loss since last snapshot
- **AOF Persistence**: Minimal data loss

### Mitigation Strategies
```python
# 1. Enable persistence
# redis.conf
save 900 1      # Save every 900 seconds if 1+ keys changed
appendonly yes  # Enable AOF persistence

# 2. Redis Sentinel for high availability
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000

# 3. Session fallback to database
def get_session_with_fallback(session_id):
    # Try Redis first
    session = r.get(f"session:{session_id}")
    if session:
        return json.loads(session)
    
    # Fallback to database
    return db.get_session(session_id)
```

## 7. Performance impact comparison

### Performance Metrics
```python
import time

# Redis performance test
def redis_performance_test():
    start = time.time()
    for i in range(10000):
        r.set(f"test:{i}", f"data:{i}")
    redis_time = time.time() - start
    
    # Database performance test
    start = time.time()
    for i in range(10000):
        db.execute("INSERT INTO sessions (id, data) VALUES (?, ?)", (i, f"data:{i}"))
    db_time = time.time() - start
    
    return f"Redis: {redis_time}s, DB: {db_time}s"
```

### Typical Performance
- **Redis**: 100,000+ operations/second
- **Database**: 1,000-10,000 operations/second
- **Cookies**: 100,000+ operations/second (local)

## 8. Session replication in distributed environment

```python
# Redis Cluster configuration
from rediscluster import RedisCluster

# Multiple Redis nodes
startup_nodes = [
    {"host": "redis-node1", "port": 7000},
    {"host": "redis-node2", "port": 7000},
    {"host": "redis-node3", "port": 7000}
]

cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# Session replication across nodes
def store_session_cluster(session_id, data):
    # Automatically distributed across cluster
    cluster.setex(f"session:{session_id}", 1800, json.dumps(data))

# Redis Sentinel for automatic failover
sentinel = redis.sentinel.Sentinel([
    ('localhost', 26379),
    ('localhost', 26380),
    ('localhost', 26381)
])

master = sentinel.master_for('mymaster')
slave = sentinel.slave_for('mymaster')
```

## 9. Real-world scenario for Redis session storage

### E-commerce Platform
```python
# High-traffic e-commerce with Redis sessions
class EcommerceSessionManager:
    def __init__(self):
        self.redis = redis.Redis(host='redis-cluster', port=6379)
    
    def create_shopping_session(self, user_id):
        session_data = {
            'user_id': user_id,
            'cart': [],
            'wishlist': [],
            'recent_views': [],
            'preferences': {},
            'last_activity': time.time()
        }
        
        session_id = str(uuid.uuid4())
        # 2-hour session for shopping
        self.redis.setex(f"session:{session_id}", 7200, json.dumps(session_data))
        return session_id
    
    def add_to_cart(self, session_id, product_id, quantity):
        session = self.get_session(session_id)
        if session:
            session['cart'].append({'product_id': product_id, 'quantity': quantity})
            session['last_activity'] = time.time()
            # Extend session on activity
            self.redis.setex(f"session:{session_id}", 7200, json.dumps(session))
    
    def get_session(self, session_id):
        data = self.redis.get(f"session:{session_id}")
        return json.loads(data) if data else None

# Usage in Flask app
@app.route('/add-to-cart/<product_id>')
def add_to_cart(product_id):
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = session_manager.create_shopping_session(current_user.id)
        response = make_response(redirect('/'))
        response.set_cookie('session_id', session_id, max_age=7200)
        return response
    
    session_manager.add_to_cart(session_id, product_id, 1)
    return redirect('/cart')
```

**Why Redis for E-commerce:**
- High concurrent user sessions
- Fast cart/wishlist updates
- Automatic session expiration
- Horizontal scaling for Black Friday traffic
- Real-time inventory integration
