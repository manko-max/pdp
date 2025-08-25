# Database Optimization

## 1. What are indexes?

**Database Indexes:**
- **Data structures** that improve query performance by creating sorted references to data
- **B-tree structures** (most common) that allow fast lookups without scanning entire tables
- **Additional storage** that trades space for speed
- **Automatic maintenance** by the database engine

```sql
-- Basic index creation
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_products_category ON products(category_id);

-- Composite index (multiple columns)
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Unique index
CREATE UNIQUE INDEX idx_user_email_unique ON users(email);

-- Partial index (only for specific conditions)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
```

**Index Types:**
```sql
-- B-tree index (default, most common)
CREATE INDEX idx_name ON table_name(column_name);

-- Hash index (equality only)
CREATE INDEX idx_hash ON table_name USING hash(column_name);

-- GiST index (geometric data)
CREATE INDEX idx_geom ON spatial_table USING gist(geometry_column);

-- GIN index (array/JSON data)
CREATE INDEX idx_tags ON products USING gin(tags);
```

## 2. How to use indexes?

```sql
-- 1. Create indexes on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_status ON orders(status);

-- 2. Use indexes in WHERE clauses
SELECT * FROM users WHERE email = 'john@example.com';  -- Uses index
SELECT * FROM orders WHERE status = 'pending';         -- Uses index

-- 3. Composite indexes for multiple conditions
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';  -- Uses composite index

-- 4. Indexes for JOIN operations
CREATE INDEX idx_orders_user_id ON orders(user_id);
SELECT u.name, o.order_date 
FROM users u 
JOIN orders o ON u.id = o.user_id;  -- Uses index on o.user_id

-- 5. Indexes for ORDER BY
CREATE INDEX idx_products_price ON products(price);
SELECT * FROM products ORDER BY price;  -- Uses index for sorting

-- 6. Indexes for GROUP BY
CREATE INDEX idx_orders_date_status ON orders(order_date, status);
SELECT order_date, COUNT(*) 
FROM orders 
GROUP BY order_date;  -- Uses index
```

**Index Usage Patterns:**
```sql
-- Good: Index can be used
SELECT * FROM users WHERE email = 'test@example.com';
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';
SELECT * FROM products WHERE price BETWEEN 10 AND 100;

-- Bad: Index cannot be used
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';  -- Function on column
SELECT * FROM orders WHERE user_id + 1 = 124;                 -- Expression on column
SELECT * FROM products WHERE name LIKE '%test%';              -- Leading wildcard
```

## 3. Which kind of columns must be indexed?

### **Primary Keys and Foreign Keys**
```sql
-- Primary keys are automatically indexed
CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- Automatically indexed
    email VARCHAR(255)
);

-- Foreign keys should be indexed
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id)  -- Should be indexed
);
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### **Frequently Queried Columns**
```sql
-- Columns used in WHERE clauses
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Columns used in JOIN conditions
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

### **Columns Used for Sorting**
```sql
-- Columns in ORDER BY
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_orders_date ON orders(order_date DESC);

-- Composite index for multiple sort columns
CREATE INDEX idx_orders_date_status ON orders(order_date, status);
```

### **Columns Used for Filtering**
```sql
-- Boolean columns
CREATE INDEX idx_users_active ON users(active);

-- Date columns
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Status columns
CREATE INDEX idx_orders_status ON orders(status);
```

### **Columns NOT to Index**
```sql
-- Low cardinality columns (few unique values)
-- CREATE INDEX idx_users_gender ON users(gender);  -- Bad: only 2-3 values

-- Rarely queried columns
-- CREATE INDEX idx_users_middle_name ON users(middle_name);  -- Bad: rarely used

-- Columns with functions/expressions
-- CREATE INDEX idx_users_email_lower ON users(LOWER(email));  -- Bad: function
```

## 4. Why can't index everything?

### **Storage Overhead**
```sql
-- Each index requires additional storage
-- Example: 1M rows table
-- Data: 100MB
-- Index on email: 20MB
-- Index on name: 15MB
-- Index on created_at: 10MB
-- Total overhead: 45MB (45% increase)
```

### **Write Performance Impact**
```sql
-- Every INSERT/UPDATE/DELETE must update indexes
-- Without indexes: 1 write operation
-- With 5 indexes: 6 write operations (1 data + 5 indexes)

-- Example: Inserting 10,000 rows
-- No indexes: 10,000 operations
-- 5 indexes: 60,000 operations (6x slower)
```

### **Maintenance Overhead**
```sql
-- Indexes need maintenance (rebuilding, statistics updates)
-- More indexes = more maintenance time
-- More indexes = more complex query planning
```

### **Memory Usage**
```sql
-- Indexes consume buffer cache memory
-- More indexes = less memory for data
-- Can lead to more disk I/O
```

**Index Cost Analysis:**
```sql
-- Calculate index size
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- Unused indexes
```

## 5. Wisdom `SELECT`

### **Select Only Needed Columns**
```sql
-- Bad: Select all columns
SELECT * FROM users WHERE email = 'test@example.com';

-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE email = 'test@example.com';
```

### **Use LIMIT for Large Results**
```sql
-- Bad: No limit
SELECT * FROM orders WHERE user_id = 123;

-- Good: With limit
SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC LIMIT 10;
```

### **Avoid SELECT DISTINCT When Possible**
```sql
-- Bad: DISTINCT on large datasets
SELECT DISTINCT category FROM products;

-- Good: Use GROUP BY
SELECT category FROM products GROUP BY category;

-- Better: If you have an index
SELECT category FROM products WHERE category IS NOT NULL;
```

### **Use EXISTS Instead of IN for Large Subqueries**
```sql
-- Bad: IN with large subquery
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE status = 'completed');

-- Good: EXISTS
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.status = 'completed'
);
```

### **Avoid SELECT COUNT(*) on Large Tables**
```sql
-- Bad: COUNT(*) on large table
SELECT COUNT(*) FROM orders;

-- Good: Use approximate count or cached count
SELECT reltuples::bigint AS estimate FROM pg_class WHERE relname = 'orders';

-- Better: Maintain count in separate table
SELECT total_orders FROM order_stats;
```

## 6. Subqueries performance

### **Correlated vs Non-Correlated Subqueries**
```sql
-- Bad: Correlated subquery (executes for each row)
SELECT u.name, (
    SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id
) as order_count
FROM users u;

-- Good: JOIN with GROUP BY
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Better: Use window function
SELECT u.name, COUNT(o.id) OVER (PARTITION BY u.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

### **Subquery Optimization Techniques**
```sql
-- Bad: Subquery in WHERE
SELECT * FROM users WHERE id IN (
    SELECT user_id FROM orders WHERE amount > 1000
);

-- Good: JOIN
SELECT DISTINCT u.* 
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.amount > 1000;

-- Better: EXISTS
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 1000
);
```

### **Common Table Expressions (CTEs)**
```sql
-- Good: Use CTEs for complex queries
WITH user_orders AS (
    SELECT user_id, COUNT(*) as order_count, SUM(amount) as total_amount
    FROM orders
    WHERE created_at >= '2024-01-01'
    GROUP BY user_id
),
active_users AS (
    SELECT * FROM users WHERE status = 'active'
)
SELECT u.name, uo.order_count, uo.total_amount
FROM active_users u
JOIN user_orders uo ON u.id = uo.user_id
WHERE uo.order_count > 5;
```

## 7. Analyze queries with `EXPLAIN`

### **Basic EXPLAIN**
```sql
-- Simple EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN with actual execution
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN with format
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT * FROM users WHERE email = 'test@example.com';
```

### **Understanding EXPLAIN Output**
```sql
-- Example EXPLAIN output analysis
EXPLAIN (ANALYZE, BUFFERS) 
SELECT u.name, COUNT(o.id) as order_count
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id, u.name;

-- Key metrics to look for:
-- - Planning time: Time to create execution plan
-- - Execution time: Time to execute the query
-- - Rows: Number of rows processed
-- - Loops: Number of times operation was performed
-- - Buffers: Memory usage
```

### **Common Performance Issues in EXPLAIN**
```sql
-- Sequential scan (bad)
EXPLAIN SELECT * FROM users WHERE name LIKE '%john%';
-- Shows: "Seq Scan on users"

-- Index scan (good)
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';
-- Shows: "Index Scan using idx_users_email"

-- Nested loop (can be slow for large datasets)
EXPLAIN SELECT u.name, o.order_date
FROM users u
JOIN orders o ON u.id = o.user_id;
-- Shows: "Nested Loop"

-- Hash join (better for large datasets)
EXPLAIN SELECT u.name, o.order_date
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';
-- Shows: "Hash Join"
```

## 8. Bulk insert

### **Single INSERT vs Bulk INSERT**
```sql
-- Bad: Multiple single inserts
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
INSERT INTO users (name, email) VALUES ('Jane', 'jane@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');

-- Good: Bulk insert
INSERT INTO users (name, email) VALUES 
    ('John', 'john@example.com'),
    ('Jane', 'jane@example.com'),
    ('Bob', 'bob@example.com');
```

### **COPY Command (PostgreSQL)**
```sql
-- Fastest: COPY command
COPY users (name, email) FROM '/path/to/data.csv' WITH (FORMAT csv);

-- COPY from program
COPY users (name, email) FROM PROGRAM 'cat /path/to/data.csv';

-- COPY with options
COPY users (name, email) FROM '/path/to/data.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');
```

### **Batch Processing**
```sql
-- Batch insert with transaction
BEGIN;
INSERT INTO users (name, email) VALUES 
    ('User1', 'user1@example.com'),
    ('User2', 'user2@example.com'),
    -- ... more rows
    ('User1000', 'user1000@example.com');
COMMIT;

-- Batch size optimization
-- Too small: Many transactions
-- Too large: Memory issues
-- Optimal: 1000-10000 rows per batch
```

### **Disable Indexes During Bulk Insert**
```sql
-- Disable indexes temporarily
ALTER TABLE users DISABLE TRIGGER ALL;
-- or
DROP INDEX idx_users_email;
-- ... bulk insert ...
-- Re-enable indexes
ALTER TABLE users ENABLE TRIGGER ALL;
-- or
CREATE INDEX idx_users_email ON users(email);
```

## 9. VACUUM

### **What is VACUUM?**
```sql
-- VACUUM reclaims storage from dead tuples
-- Dead tuples: rows that are deleted or updated

-- Basic VACUUM
VACUUM users;

-- VACUUM ANALYZE (updates statistics too)
VACUUM ANALYZE users;

-- VACUUM FULL (rewrites entire table)
VACUUM FULL users;

-- Auto VACUUM (automatic)
-- Configured in postgresql.conf
autovacuum = on
autovacuum_vacuum_threshold = 50
autovacuum_analyze_threshold = 50
```

### **When to Use VACUUM**
```sql
-- After large DELETE operations
DELETE FROM old_logs WHERE created_at < '2023-01-01';
VACUUM logs;

-- After large UPDATE operations
UPDATE users SET status = 'inactive' WHERE last_login < '2023-01-01';
VACUUM users;

-- Regular maintenance
-- Run VACUUM ANALYZE weekly on active tables
VACUUM ANALYZE users, orders, products;
```

### **VACUUM Monitoring**
```sql
-- Check table bloat
SELECT 
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    round(n_dead_tup * 100.0 / nullif(n_live_tup + n_dead_tup, 0), 2) as dead_percentage
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY dead_percentage DESC;

-- Check last VACUUM
SELECT 
    schemaname,
    tablename,
    last_vacuum,
    last_autovacuum,
    vacuum_count,
    autovacuum_count
FROM pg_stat_user_tables;
```

## 10. Calculations balance

### **What to Execute at DB Level?**

**Good for DB Level:**
```sql
-- Aggregations
SELECT user_id, COUNT(*), SUM(amount), AVG(amount)
FROM orders
GROUP BY user_id;

-- Mathematical calculations
SELECT 
    product_id,
    price,
    discount,
    price * (1 - discount/100) as final_price
FROM products;

-- Date calculations
SELECT 
    order_date,
    order_date + INTERVAL '30 days' as due_date,
    EXTRACT(YEAR FROM order_date) as order_year
FROM orders;

-- String operations
SELECT 
    name,
    UPPER(name) as upper_name,
    LENGTH(name) as name_length
FROM users;

-- Conditional logic
SELECT 
    amount,
    CASE 
        WHEN amount > 1000 THEN 'high'
        WHEN amount > 100 THEN 'medium'
        ELSE 'low'
    END as amount_category
FROM orders;
```

**Bad for DB Level:**
```sql
-- Complex business logic
-- Complex data transformations
-- External API calls
-- File operations
-- Complex algorithms
```

### **What Calculations Move to Programming Language Level?**

**Good for Application Level:**
```python
# Complex business logic
def calculate_tax(amount, country, user_type):
    if country == 'US':
        if user_type == 'business':
            return amount * 0.08
        else:
            return amount * 0.06
    elif country == 'CA':
        return amount * 0.13
    # ... complex logic

# Data transformations
def transform_user_data(user_data):
    return {
        'full_name': f"{user_data['first_name']} {user_data['last_name']}",
        'age': calculate_age(user_data['birth_date']),
        'address': format_address(user_data['address_components'])
    }

# External integrations
def enrich_user_data(user_id):
    user = get_user_from_db(user_id)
    user['credit_score'] = call_credit_api(user_id)
    user['social_media'] = get_social_media_data(user_id)
    return user

# Complex algorithms
def recommend_products(user_id, user_behavior):
    # Machine learning algorithms
    # Complex scoring systems
    # Recommendation engines
    pass
```

## 11. MATERIALIZED VIEWS

### **What are Materialized Views?**
```sql
-- Materialized views store query results physically
-- Unlike regular views, they don't recalculate on each access

-- Create materialized view
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT 
    u.id,
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_amount,
    AVG(o.amount) as avg_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Query materialized view
SELECT * FROM user_order_summary WHERE order_count > 5;
```

### **When to Use Materialized Views**
```sql
-- Expensive aggregations
CREATE MATERIALIZED VIEW daily_sales AS
SELECT 
    DATE(created_at) as sale_date,
    COUNT(*) as total_orders,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_order_value
FROM orders
GROUP BY DATE(created_at);

-- Complex joins
CREATE MATERIALIZED VIEW product_performance AS
SELECT 
    p.id,
    p.name,
    p.category,
    COUNT(oi.id) as times_ordered,
    SUM(oi.quantity) as total_quantity,
    AVG(oi.price) as avg_price
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed'
GROUP BY p.id, p.name, p.category;
```

### **Refreshing Materialized Views**
```sql
-- Manual refresh
REFRESH MATERIALIZED VIEW user_order_summary;

-- Concurrent refresh (PostgreSQL 9.4+)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_order_summary;

-- Scheduled refresh
-- Use cron job or application scheduler
-- Example: Refresh daily at 2 AM
-- 0 2 * * * psql -d mydb -c "REFRESH MATERIALIZED VIEW daily_sales;"
```

### **Materialized View vs Regular View**
```sql
-- Regular view (virtual)
CREATE VIEW user_order_summary AS
SELECT 
    u.id,
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Materialized view (physical)
CREATE MATERIALIZED VIEW user_order_summary_mv AS
SELECT 
    u.id,
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Performance comparison
-- Regular view: Recalculates every time (slow)
-- Materialized view: Stored result (fast, but needs refresh)
```

### **Indexes on Materialized Views**
```sql
-- Create indexes on materialized views for better performance
CREATE INDEX idx_user_order_summary_id ON user_order_summary(id);
CREATE INDEX idx_user_order_summary_count ON user_order_summary(order_count);

-- Query with index
SELECT * FROM user_order_summary WHERE order_count > 10;
```

### **Best Practices for Materialized Views**
```sql
-- Use for expensive, frequently-accessed queries
-- Refresh regularly based on data freshness requirements
-- Monitor storage usage (materialized views take space)
-- Consider partitioning for large materialized views
-- Use concurrent refresh to avoid blocking reads

-- Example: Partitioned materialized view
CREATE MATERIALIZED VIEW monthly_sales_2024 AS
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as orders,
    SUM(amount) as revenue
FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
GROUP BY DATE_TRUNC('month', created_at);
```
