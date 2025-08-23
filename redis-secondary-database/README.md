# Redis as Secondary Database

## 1. How Redis operates as a key-value database

**Redis Key-Value Model:**
- **Keys**: Unique identifiers (strings) that map to values
- **Values**: Data stored in various formats (strings, hashes, lists, sets, etc.)
- **In-memory storage**: Primary storage in RAM for fast access
- **Optional persistence**: Can save to disk (RDB snapshots, AOF logs)
- **Atomic operations**: All operations are atomic and thread-safe
- **TTL support**: Automatic expiration of keys

```python
import redis

# Basic key-value operations
r = redis.Redis(host='localhost', port=6379, db=0)

# Set and get values
r.set('user:123:name', 'John Doe')
r.set('user:123:email', 'john@example.com')
r.setex('user:123:session', 3600, 'session_token')  # With TTL

# Get values
name = r.get('user:123:name')  # Returns: b'John Doe'
email = r.get('user:123:email')  # Returns: b'john@example.com'
```

## 2. Data types supported by Redis and their differences

### String
```python
# Basic string operations
r.set('counter', 0)
r.incr('counter')  # Increment by 1
r.incrby('counter', 5)  # Increment by 5
r.decr('counter')  # Decrement by 1

# String manipulation
r.set('message', 'Hello World')
r.append('message', '!')  # Append to string
r.getrange('message', 0, 4)  # Get substring: b'Hello'
r.setrange('message', 6, 'Redis')  # Replace substring
```

### Hash
```python
# Hash operations - store object-like data
r.hset('user:123', 'name', 'John Doe')
r.hset('user:123', 'email', 'john@example.com')
r.hset('user:123', 'age', 30)

# Get hash fields
r.hget('user:123', 'name')  # Returns: b'John Doe'
r.hgetall('user:123')  # Returns all fields as dict

# Hash operations
r.hincrby('user:123', 'age', 1)  # Increment field
r.hdel('user:123', 'age')  # Delete field
r.hexists('user:123', 'email')  # Check if field exists
```

### List
```python
# List operations - ordered collections
r.lpush('queue:emails', 'email1@example.com')
r.rpush('queue:emails', 'email2@example.com')
r.lpush('queue:emails', 'email3@example.com')

# Get list elements
r.lrange('queue:emails', 0, -1)  # Get all elements
r.lpop('queue:emails')  # Remove and return leftmost
r.rpop('queue:emails')  # Remove and return rightmost

# List manipulation
r.linsert('queue:emails', 'BEFORE', 'email2@example.com', 'email1.5@example.com')
r.lrem('queue:emails', 1, 'email2@example.com')  # Remove element
```

### Set
```python
# Set operations - unordered unique collections
r.sadd('user:123:tags', 'python', 'redis', 'database')
r.sadd('user:456:tags', 'java', 'redis', 'spring')

# Set operations
r.smembers('user:123:tags')  # Get all members
r.sismember('user:123:tags', 'python')  # Check membership
r.sinter('user:123:tags', 'user:456:tags')  # Intersection
r.sunion('user:123:tags', 'user:456:tags')  # Union
r.sdiff('user:123:tags', 'user:456:tags')  # Difference
```

### Sorted Set
```python
# Sorted set operations - ordered by score
r.zadd('leaderboard', {'player1': 100, 'player2': 200, 'player3': 150})

# Get sorted elements
r.zrange('leaderboard', 0, -1)  # Get all by rank
r.zrevrange('leaderboard', 0, -1)  # Get all by reverse rank
r.zrangebyscore('leaderboard', 100, 200)  # Get by score range

# Sorted set operations
r.zincrby('leaderboard', 50, 'player1')  # Increment score
r.zrank('leaderboard', 'player2')  # Get rank
r.zscore('leaderboard', 'player2')  # Get score
```

## 3. How to store and retrieve data in Redis

```python
class RedisDataManager:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
    
    def store_user_data(self, user_id, user_data):
        """Store user data using hash"""
        key = f"user:{user_id}"
        self.redis.hmset(key, user_data)
        self.redis.expire(key, 86400)  # Expire in 24 hours
        return True
    
    def get_user_data(self, user_id):
        """Retrieve user data"""
        key = f"user:{user_id}"
        data = self.redis.hgetall(key)
        return data if data else None
    
    def store_cache_data(self, key, data, ttl=3600):
        """Store cache data with TTL"""
        self.redis.setex(key, ttl, json.dumps(data))
    
    def get_cache_data(self, key):
        """Retrieve cache data"""
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def store_session_data(self, session_id, session_data):
        """Store session data"""
        key = f"session:{session_id}"
        self.redis.setex(key, 1800, json.dumps(session_data))  # 30 min TTL
    
    def get_session_data(self, session_id):
        """Retrieve session data"""
        key = f"session:{session_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None

# Usage
data_manager = RedisDataManager()

# Store user data
user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': '30',
    'last_login': str(time.time())
}
data_manager.store_user_data(123, user_data)

# Retrieve user data
user = data_manager.get_user_data(123)
```

## 4. How and why to use Redis hash to store an object

```python
class UserObject:
    def __init__(self, user_id, name, email, age):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'age': str(self.age),
            'created_at': str(time.time())
        }

class RedisObjectStorage:
    def __init__(self):
        self.redis = redis.Redis()
    
    def store_object(self, obj, prefix='object'):
        """Store object as hash"""
        key = f"{prefix}:{obj.user_id}"
        data = obj.to_dict()
        self.redis.hmset(key, data)
        return key
    
    def get_object(self, object_id, prefix='object'):
        """Retrieve object from hash"""
        key = f"{prefix}:{object_id}"
        data = self.redis.hgetall(key)
        if data:
            return UserObject(
                user_id=object_id,
                name=data[b'name'].decode(),
                email=data[b'email'].decode(),
                age=int(data[b'age'].decode())
            )
        return None
    
    def update_object_field(self, object_id, field, value, prefix='object'):
        """Update specific field of object"""
        key = f"{prefix}:{object_id}"
        self.redis.hset(key, field, value)
    
    def delete_object(self, object_id, prefix='object'):
        """Delete object"""
        key = f"{prefix}:{object_id}"
        self.redis.delete(key)

# Usage
user = UserObject(123, 'John Doe', 'john@example.com', 30)
storage = RedisObjectStorage()

# Store object
storage.store_object(user, 'user')

# Retrieve object
retrieved_user = storage.get_object(123, 'user')

# Update specific field
storage.update_object_field(123, 'age', '31', 'user')
```

**Why use hashes for objects:**
- **Memory efficiency**: More efficient than separate keys
- **Atomic updates**: Update individual fields atomically
- **Batch operations**: Get/set multiple fields at once
- **Field-level expiration**: Can expire individual fields (with Redis 4.0+)

## 5. How Redis handles memory exhaustion

```python
class RedisMemoryManager:
    def __init__(self):
        self.redis = redis.Redis()
    
    def get_memory_info(self):
        """Get Redis memory information"""
        info = self.redis.info('memory')
        return {
            'used_memory': info['used_memory'],
            'used_memory_human': info['used_memory_human'],
            'maxmemory': info.get('maxmemory', 0),
            'maxmemory_policy': info.get('maxmemory_policy', 'noeviction')
        }
    
    def configure_memory_policy(self, policy='allkeys-lru'):
        """Configure memory eviction policy"""
        # Available policies:
        # noeviction, allkeys-lru, volatile-lru, allkeys-random, volatile-random, volatile-ttl
        self.redis.config_set('maxmemory-policy', policy)
    
    def set_max_memory(self, bytes_limit):
        """Set maximum memory limit"""
        self.redis.config_set('maxmemory', bytes_limit)
    
    def monitor_memory_usage(self):
        """Monitor memory usage and take action if needed"""
        info = self.get_memory_info()
        used_memory = info['used_memory']
        max_memory = info['maxmemory']
        
        if max_memory > 0 and used_memory > max_memory * 0.9:  # 90% threshold
            print(f"Memory usage high: {used_memory}/{max_memory}")
            self.cleanup_old_data()
    
    def cleanup_old_data(self):
        """Clean up old data to free memory"""
        # Delete expired keys
        self.redis.eval("""
            local keys = redis.call('keys', ARGV[1])
            for i=1, #keys do
                redis.call('expire', keys[i], 0)
            end
        """, 0, 'temp:*')
        
        # Delete old cache entries
        self.redis.eval("""
            local keys = redis.call('keys', 'cache:*')
            for i=1, #keys do
                local ttl = redis.call('ttl', keys[i])
                if ttl == -1 then  -- No expiration set
                    redis.call('del', keys[i])
                end
            end
        """, 0)

# Memory policies explanation
MEMORY_POLICIES = {
    'noeviction': 'Return error when memory limit is reached',
    'allkeys-lru': 'Remove least recently used keys',
    'volatile-lru': 'Remove least recently used keys with expiration',
    'allkeys-random': 'Remove random keys',
    'volatile-random': 'Remove random keys with expiration',
    'volatile-ttl': 'Remove keys with shortest TTL'
}
```

## 6. Managing key expiration in Redis

```python
class RedisExpirationManager:
    def __init__(self):
        self.redis = redis.Redis()
    
    def set_with_expiration(self, key, value, ttl_seconds):
        """Set key with expiration"""
        self.redis.setex(key, ttl_seconds, value)
    
    def set_hash_with_expiration(self, key, data, ttl_seconds):
        """Set hash with expiration"""
        self.redis.hmset(key, data)
        self.redis.expire(key, ttl_seconds)
    
    def extend_expiration(self, key, additional_seconds):
        """Extend key expiration"""
        current_ttl = self.redis.ttl(key)
        if current_ttl > 0:
            self.redis.expire(key, current_ttl + additional_seconds)
    
    def get_expiration_info(self, key):
        """Get expiration information for key"""
        ttl = self.redis.ttl(key)
        if ttl == -1:
            return "No expiration set"
        elif ttl == -2:
            return "Key does not exist"
        else:
            return f"Expires in {ttl} seconds"
    
    def set_expiration_pattern(self, pattern, ttl_seconds):
        """Set expiration for all keys matching pattern"""
        keys = self.redis.keys(pattern)
        for key in keys:
            self.redis.expire(key, ttl_seconds)
    
    def cleanup_expired_keys(self):
        """Manually trigger expired key cleanup"""
        # Redis automatically removes expired keys, but you can trigger cleanup
        self.redis.eval("""
            local keys = redis.call('keys', ARGV[1])
            for i=1, #keys do
                redis.call('expire', keys[i], 0)
            end
        """, 0, '*')

# Usage examples
exp_manager = RedisExpirationManager()

# Set different expiration times
exp_manager.set_with_expiration('session:123', 'session_data', 1800)  # 30 min
exp_manager.set_with_expiration('cache:user:123', 'user_data', 3600)  # 1 hour
exp_manager.set_with_expiration('temp:upload:456', 'file_data', 300)  # 5 min

# Extend expiration on activity
exp_manager.extend_expiration('session:123', 1800)  # Extend by 30 min

# Set expiration for pattern
exp_manager.set_expiration_pattern('temp:*', 600)  # 10 min for all temp keys
```

## 7. Advantages and disadvantages vs MongoDB/DynamoDB

### Redis Advantages
- **Speed**: Sub-millisecond access times
- **Simplicity**: Simple key-value model
- **Memory efficiency**: Optimized data structures
- **Atomic operations**: All operations are atomic
- **TTL support**: Built-in expiration
- **Low latency**: Perfect for caching

### Redis Disadvantages
- **Memory limitation**: All data in RAM
- **Limited querying**: No complex queries like SQL
- **No schema**: No data validation
- **Limited persistence**: Optional disk storage
- **Single-threaded**: Limited CPU utilization

### Comparison Table
| Feature | Redis | MongoDB | DynamoDB |
|---------|-------|---------|----------|
| **Data Model** | Key-Value | Document | Key-Value/Document |
| **Storage** | Memory + Optional Disk | Disk | Cloud |
| **Querying** | Basic | Advanced | Basic |
| **Scalability** | Horizontal | Horizontal | Auto-scaling |
| **Consistency** | Strong | Eventual | Configurable |
| **Cost** | Low | Medium | Pay-per-use |
| **Setup** | Simple | Medium | Simple |

## 8. Ensuring data consistency and reliability

```python
class ReliableRedisStorage:
    def __init__(self):
        self.redis = redis.Redis()
        self.backup_redis = redis.Redis(host='backup-server', port=6379)
    
    def store_with_backup(self, key, value, ttl=None):
        """Store data with backup for reliability"""
        try:
            # Store in primary Redis
            if ttl:
                self.redis.setex(key, ttl, value)
            else:
                self.redis.set(key, value)
            
            # Backup to secondary Redis
            if ttl:
                self.backup_redis.setex(key, ttl, value)
            else:
                self.backup_redis.set(key, value)
            
            return True
        except Exception as e:
            print(f"Storage error: {e}")
            return False
    
    def get_with_fallback(self, key):
        """Get data with fallback to backup"""
        try:
            # Try primary Redis
            value = self.redis.get(key)
            if value:
                return value
            
            # Fallback to backup
            value = self.backup_redis.get(key)
            if value:
                # Restore to primary
                self.redis.set(key, value)
                return value
            
            return None
        except Exception as e:
            print(f"Retrieval error: {e}")
            return None
    
    def atomic_operation(self, key, operation_func):
        """Perform atomic operation with retry"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self.redis.pipeline() as pipe:
                    # Watch key for changes
                    pipe.watch(key)
                    
                    # Get current value
                    current_value = pipe.get(key)
                    
                    # Perform operation
                    new_value = operation_func(current_value)
                    
                    # Execute transaction
                    pipe.multi()
                    pipe.set(key, new_value)
                    pipe.execute()
                    
                    return new_value
            except redis.WatchError:
                if attempt == max_retries - 1:
                    raise
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
    
    def enable_persistence(self):
        """Configure Redis persistence"""
        # Enable RDB snapshots
        self.redis.config_set('save', '900 1 300 10 60 10000')
        
        # Enable AOF persistence
        self.redis.config_set('appendonly', 'yes')
        self.redis.config_set('appendfsync', 'everysec')
    
    def verify_data_integrity(self, key):
        """Verify data integrity between primary and backup"""
        primary_value = self.redis.get(key)
        backup_value = self.backup_redis.get(key)
        
        if primary_value != backup_value:
            print(f"Data inconsistency detected for key: {key}")
            return False
        return True

# Usage
reliable_storage = ReliableRedisStorage()

# Store with backup
reliable_storage.store_with_backup('user:123', 'user_data', 3600)

# Get with fallback
data = reliable_storage.get_with_fallback('user:123')

# Atomic operation
def increment_counter(current_value):
    current = int(current_value) if current_value else 0
    return str(current + 1)

new_value = reliable_storage.atomic_operation('counter', increment_counter)
```

## 9. Searching for keys based on values in Redis

```python
class RedisSearchManager:
    def __init__(self):
        self.redis = redis.Redis()
    
    def search_by_pattern(self, pattern):
        """Search keys by pattern"""
        return self.redis.keys(pattern)
    
    def search_by_value(self, value):
        """Search for keys with specific value (inefficient)"""
        matching_keys = []
        all_keys = self.redis.keys('*')
        
        for key in all_keys:
            if self.redis.get(key) == value:
                matching_keys.append(key)
        
        return matching_keys
    
    def search_hash_by_field_value(self, hash_pattern, field, value):
        """Search hashes by field value"""
        matching_keys = []
        hash_keys = self.redis.keys(hash_pattern)
        
        for key in hash_keys:
            field_value = self.redis.hget(key, field)
            if field_value == value:
                matching_keys.append(key)
        
        return matching_keys
    
    def create_search_index(self, key_pattern, field_name):
        """Create search index using sorted set"""
        index_key = f"index:{field_name}"
        keys = self.redis.keys(key_pattern)
        
        for key in keys:
            value = self.redis.hget(key, field_name)
            if value:
                # Store key in sorted set with value as score
                self.redis.zadd(index_key, {key: float(value)})
    
    def search_by_index(self, field_name, min_value, max_value):
        """Search using index"""
        index_key = f"index:{field_name}"
        return self.redis.zrangebyscore(index_key, min_value, max_value)
    
    def search_by_tag(self, tag):
        """Search by tag using sets"""
        tag_key = f"tag:{tag}"
        return list(self.redis.smembers(tag_key))
    
    def add_tag_to_key(self, key, tag):
        """Add tag to key"""
        tag_key = f"tag:{tag}"
        self.redis.sadd(tag_key, key)
    
    def remove_tag_from_key(self, key, tag):
        """Remove tag from key"""
        tag_key = f"tag:{tag}"
        self.redis.srem(tag_key, key)

# Usage
search_manager = RedisSearchManager()

# Search by pattern
user_keys = search_manager.search_by_pattern('user:*')
session_keys = search_manager.search_by_pattern('session:*')

# Create search index
search_manager.create_search_index('user:*', 'age')

# Search by age range
young_users = search_manager.search_by_index('age', 18, 25)
adult_users = search_manager.search_by_index('age', 26, 65)

# Tag-based search
search_manager.add_tag_to_key('user:123', 'premium')
search_manager.add_tag_to_key('user:456', 'premium')
premium_users = search_manager.search_by_tag('premium')
```

## 10. Real-world scenario for Redis as key-value database

### E-commerce Caching System
```python
class EcommerceCacheSystem:
    def __init__(self):
        self.redis = redis.Redis()
        self.cache_ttl = {
            'product': 3600,      # 1 hour
            'user': 1800,         # 30 minutes
            'cart': 7200,         # 2 hours
            'inventory': 300,     # 5 minutes
            'search': 1800        # 30 minutes
        }
    
    def cache_product(self, product_id, product_data):
        """Cache product information"""
        key = f"product:{product_id}"
        self.redis.setex(key, self.cache_ttl['product'], json.dumps(product_data))
    
    def get_cached_product(self, product_id):
        """Get cached product information"""
        key = f"product:{product_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def cache_user_session(self, user_id, session_data):
        """Cache user session data"""
        key = f"user:{user_id}:session"
        self.redis.setex(key, self.cache_ttl['user'], json.dumps(session_data))
    
    def cache_shopping_cart(self, user_id, cart_data):
        """Cache shopping cart"""
        key = f"cart:{user_id}"
        self.redis.setex(key, self.cache_ttl['cart'], json.dumps(cart_data))
    
    def cache_inventory(self, product_id, quantity):
        """Cache inventory levels"""
        key = f"inventory:{product_id}"
        self.redis.setex(key, self.cache_ttl['inventory'], quantity)
    
    def cache_search_results(self, query, results):
        """Cache search results"""
        key = f"search:{hash(query)}"
        self.redis.setex(key, self.cache_ttl['search'], json.dumps(results))
    
    def get_cached_search_results(self, query):
        """Get cached search results"""
        key = f"search:{hash(query)}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def invalidate_product_cache(self, product_id):
        """Invalidate product cache when updated"""
        key = f"product:{product_id}"
        self.redis.delete(key)
    
    def get_cache_stats(self):
        """Get cache statistics"""
        stats = {}
        for cache_type in self.cache_ttl.keys():
            pattern = f"{cache_type}:*"
            keys = self.redis.keys(pattern)
            stats[cache_type] = len(keys)
        return stats

# Usage in Flask application
@app.route('/product/<product_id>')
def get_product(product_id):
    cache_system = EcommerceCacheSystem()
    
    # Try to get from cache first
    cached_product = cache_system.get_cached_product(product_id)
    if cached_product:
        return jsonify(cached_product)
    
    # If not in cache, get from database
    product = database.get_product(product_id)
    if product:
        # Cache the product
        cache_system.cache_product(product_id, product)
        return jsonify(product)
    
    return jsonify({'error': 'Product not found'}), 404

@app.route('/search')
def search_products():
    query = request.args.get('q', '')
    cache_system = EcommerceCacheSystem()
    
    # Try cached results
    cached_results = cache_system.get_cached_search_results(query)
    if cached_results:
        return jsonify(cached_results)
    
    # Perform search
    results = database.search_products(query)
    
    # Cache results
    cache_system.cache_search_results(query, results)
    
    return jsonify(results)
```

**Why Redis for E-commerce Caching:**
- **Fast product lookups**: Sub-millisecond access to product data
- **Session management**: Quick user session retrieval
- **Shopping cart persistence**: Fast cart operations
- **Inventory caching**: Real-time inventory levels
- **Search result caching**: Reduce database load
- **Cache invalidation**: Quick cache updates when data changes
