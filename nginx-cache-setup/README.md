# Nginx Cache Setup - Complete Guide

## Table of Contents
1. [What is Nginx?](#what-is-nginx)
2. [What is Nginx Cache?](#what-is-nginx-cache)
3. [Why and When to Use Nginx Cache?](#why-and-when-to-use-nginx-cache)
4. [Basic Nginx Caching Setup](#basic-nginx-caching-setup)
5. [Advanced Configuration](#advanced-configuration)
6. [Cache Invalidation](#cache-invalidation)
7. [Monitoring and Debugging](#monitoring-and-debugging)
8. [Best Practices](#best-practices)
9. [Docker Setup](#docker-setup)
10. [Practical Examples](#practical-examples)

## What is Nginx?

### Overview
Nginx (pronounced "engine-x") is a high-performance web server, reverse proxy, and load balancer. It's known for its:

- **High Performance**: Handles thousands of concurrent connections efficiently
- **Low Memory Usage**: Event-driven architecture
- **Reverse Proxy**: Routes requests to backend servers
- **Load Balancing**: Distributes traffic across multiple servers
- **SSL Termination**: Handles HTTPS encryption/decryption
- **Static File Serving**: Serves static content directly
- **Caching**: Stores frequently requested content

### Key Features
```nginx
# Nginx can act as:
# 1. Web Server - serves static files
# 2. Reverse Proxy - forwards requests to backend
# 3. Load Balancer - distributes traffic
# 4. Cache Server - stores responses
# 5. SSL Terminator - handles HTTPS
```

### Architecture
```
Client Request → Nginx → Backend Server
                ↓
            Cache Layer
                ↓
            Static Files
```

## What is Nginx Cache?

### Definition
Nginx Cache is a mechanism that stores HTTP responses from backend servers in memory or on disk, allowing Nginx to serve cached content directly without forwarding requests to the backend.

### How it Works
```
1. Client requests /api/data
2. Nginx checks cache
3. If cached: Return cached response (fast)
4. If not cached: Forward to backend, cache response, return to client
```

### Cache Storage
- **Memory**: Fast access, limited by RAM
- **Disk**: Persistent, limited by disk space
- **Hybrid**: Hot content in memory, cold content on disk

### Cache Zones
```nginx
# Define cache zones
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
```

## Why and When to Use Nginx Cache?

### Benefits

#### 1. **Performance Improvement**
- **Faster Response Times**: Cached content served directly from Nginx
- **Reduced Backend Load**: Fewer requests reach backend servers
- **Better User Experience**: Lower latency for cached content

#### 2. **Cost Reduction**
- **Lower Server Costs**: Fewer backend servers needed
- **Reduced Bandwidth**: Less data transfer from backend
- **Energy Savings**: Less computational load

#### 3. **Scalability**
- **Handle Traffic Spikes**: Cache absorbs sudden load increases
- **Global Distribution**: CDN-like functionality
- **Backend Protection**: Prevents backend overload

### When to Use

#### ✅ **Good Use Cases**
- **Static Content**: Images, CSS, JS files
- **API Responses**: Frequently requested data
- **Database Queries**: Expensive operations
- **Third-party APIs**: External service calls
- **RSS Feeds**: News, blog feeds
- **Search Results**: Cached search queries

#### ❌ **Avoid Caching**
- **User-specific Content**: Personal data, user sessions
- **Real-time Data**: Stock prices, live chat
- **Frequently Changing Content**: Dynamic data
- **Large Files**: Videos, large downloads
- **Sensitive Data**: Authentication tokens, passwords

### Performance Impact
```
Without Cache:
Client → Nginx → Backend → Database → Backend → Nginx → Client
Time: 500ms

With Cache:
Client → Nginx (Cache Hit) → Client
Time: 10ms
```

## Basic Nginx Caching Setup

### 1. Install Nginx
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx

# Docker
docker run -d -p 80:80 nginx
```

### 2. Basic Configuration
```nginx
# /etc/nginx/nginx.conf
http {
    # Define cache zone
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
    
    server {
        listen 80;
        server_name example.com;
        
        # Enable caching
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        
        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### 3. Cache Configuration Parameters
```nginx
# Cache zone definition
proxy_cache_path /var/cache/nginx 
    levels=1:2                    # Directory structure: 1 level deep, 2 characters
    keys_zone=my_cache:10m        # Cache zone name and size in memory
    max_size=1g                   # Maximum disk usage
    inactive=60m                  # Remove unused cache after 60 minutes
    use_temp_path=off;            # Don't use temporary path

# Cache settings
proxy_cache my_cache;             # Use the cache zone
proxy_cache_valid 200 302 10m;    # Cache successful responses for 10 minutes
proxy_cache_valid 404 1m;         # Cache 404 errors for 1 minute
proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
```

### 4. Complete Basic Setup
```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    server_name example.com;
    
    # Cache configuration
    proxy_cache my_cache;
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404 1m;
    proxy_cache_use_stale error timeout updating;
    
    # Cache headers
    add_header X-Cache-Status $upstream_cache_status;
    
    # Backend configuration
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files (direct serving)
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API endpoints with different cache rules
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_cache_valid 200 5m;
        proxy_cache_valid 404 1m;
        proxy_cache_key $scheme$proxy_host$request_uri;
    }
}
```

## Advanced Configuration

### 1. Multiple Cache Zones
```nginx
http {
    # Different cache zones for different content types
    proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api_cache:50m max_size=2g inactive=30m;
    proxy_cache_path /var/cache/nginx/static levels=1:2 keys_zone=static_cache:100m max_size=5g inactive=1h;
    proxy_cache_path /var/cache/nginx/dynamic levels=1:2 keys_zone=dynamic_cache:20m max_size=500m inactive=5m;
    
    server {
        # API caching
        location /api/ {
            proxy_cache api_cache;
            proxy_cache_valid 200 5m;
            proxy_cache_key $scheme$proxy_host$request_uri$args;
        }
        
        # Static content caching
        location /static/ {
            proxy_cache static_cache;
            proxy_cache_valid 200 1h;
            proxy_cache_key $scheme$proxy_host$request_uri;
        }
        
        # Dynamic content caching
        location /dynamic/ {
            proxy_cache dynamic_cache;
            proxy_cache_valid 200 1m;
            proxy_cache_key $scheme$proxy_host$request_uri$args;
        }
    }
}
```

### 2. Conditional Caching
```nginx
server {
    # Cache based on request method
    location /api/ {
        proxy_pass http://backend;
        
        # Only cache GET requests
        proxy_cache my_cache;
        proxy_cache_methods GET HEAD;
        proxy_cache_valid 200 10m;
        
        # Don't cache POST, PUT, DELETE
        proxy_cache_bypass $request_method;
    }
    
    # Cache based on user agent
    location /mobile/ {
        proxy_pass http://backend;
        proxy_cache my_cache;
        
        # Different cache for mobile
        proxy_cache_key $scheme$proxy_host$request_uri$http_user_agent;
        proxy_cache_valid 200 5m;
    }
    
    # Cache based on query parameters
    location /search/ {
        proxy_pass http://backend;
        proxy_cache my_cache;
        
        # Include query parameters in cache key
        proxy_cache_key $scheme$proxy_host$request_uri$args;
        proxy_cache_valid 200 15m;
    }
}
```

### 3. Cache Purging
```nginx
# Allow cache purging from specific IPs
location ~ /purge(/.*) {
    allow 127.0.0.1;
    allow 192.168.1.0/24;
    deny all;
    
    proxy_cache_purge my_cache $scheme$proxy_host$1;
}
```

### 4. Advanced Cache Headers
```nginx
server {
    location / {
        proxy_pass http://backend;
        proxy_cache my_cache;
        
        # Cache control
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_valid any 1m;
        
        # Cache bypass conditions
        proxy_cache_bypass $cookie_nocache $arg_nocache;
        proxy_no_cache $cookie_nocache $arg_nocache;
        
        # Cache key customization
        proxy_cache_key $scheme$proxy_host$request_uri$args;
        
        # Stale content handling
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        
        # Cache headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Cache-Key $proxy_cache_key;
    }
}
```

## Cache Invalidation

### 1. Manual Cache Purging
```bash
# Purge specific URL
curl -X PURGE http://example.com/purge/api/data

# Purge all cache
sudo rm -rf /var/cache/nginx/*
sudo nginx -s reload
```

### 2. Programmatic Cache Invalidation
```python
# Python script to purge cache
import requests

def purge_cache(url):
    purge_url = f"http://nginx-server/purge{url}"
    response = requests.get(purge_url)
    return response.status_code == 200

# Usage
purge_cache("/api/users/123")
```

### 3. Cache Invalidation Headers
```nginx
# Invalidate cache based on headers
location /api/ {
    proxy_pass http://backend;
    proxy_cache my_cache;
    
    # Don't cache if backend sends no-cache header
    proxy_cache_bypass $http_pragma $http_authorization;
    proxy_no_cache $http_pragma $http_authorization;
}
```

### 4. Time-based Invalidation
```nginx
# Different cache times for different content
location /api/users/ {
    proxy_cache my_cache;
    proxy_cache_valid 200 5m;    # User data changes frequently
}

location /api/config/ {
    proxy_cache my_cache;
    proxy_cache_valid 200 1h;    # Config changes rarely
}

location /api/static-data/ {
    proxy_cache my_cache;
    proxy_cache_valid 200 1d;    # Static data rarely changes
}
```

## Monitoring and Debugging

### 1. Cache Status Headers
```nginx
# Add cache status to response headers
add_header X-Cache-Status $upstream_cache_status;
add_header X-Cache-Key $proxy_cache_key;
add_header X-Cache-Date $upstream_http_date;
```

### 2. Cache Status Values
```
MISS: Content not in cache, fetched from backend
HIT: Content served from cache
EXPIRED: Content expired, fetched from backend
STALE: Serving stale content while updating
UPDATING: Currently updating cache
REVALIDATED: Content revalidated with backend
BYPASS: Cache bypassed due to conditions
```

### 3. Logging Configuration
```nginx
# Custom log format for cache monitoring
log_format cache_log '$remote_addr - $remote_user [$time_local] '
                     '"$request" $status $body_bytes_sent '
                     '"$http_referer" "$http_user_agent" '
                     'cache_status=$upstream_cache_status '
                     'cache_key=$proxy_cache_key';

server {
    access_log /var/log/nginx/cache.log cache_log;
    
    location / {
        proxy_pass http://backend;
        proxy_cache my_cache;
        # ... cache configuration
    }
}
```

### 4. Monitoring Scripts
```bash
#!/bin/bash
# Monitor cache hit ratio

LOG_FILE="/var/log/nginx/cache.log"
TOTAL_REQUESTS=$(grep -c "cache_status=" $LOG_FILE)
HIT_REQUESTS=$(grep -c "cache_status=HIT" $LOG_FILE)
MISS_REQUESTS=$(grep -c "cache_status=MISS" $LOG_FILE)

if [ $TOTAL_REQUESTS -gt 0 ]; then
    HIT_RATIO=$(echo "scale=2; $HIT_REQUESTS * 100 / $TOTAL_REQUESTS" | bc)
    echo "Cache Hit Ratio: $HIT_RATIO%"
    echo "Total Requests: $TOTAL_REQUESTS"
    echo "Cache Hits: $HIT_REQUESTS"
    echo "Cache Misses: $MISS_REQUESTS"
fi
```

## Best Practices

### 1. Cache Key Design
```nginx
# Good cache keys
proxy_cache_key $scheme$proxy_host$request_uri$args;  # Include query params
proxy_cache_key $scheme$proxy_host$request_uri$http_user_agent;  # User-specific

# Avoid overly complex keys
proxy_cache_key $scheme$proxy_host$request_uri$args$http_accept$http_accept_language;  # Too complex
```

### 2. Cache Size Management
```nginx
# Appropriate cache sizes
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:50m max_size=2g inactive=30m;
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=static_cache:100m max_size=5g inactive=1h;

# Monitor disk usage
df -h /var/cache/nginx/
```

### 3. Security Considerations
```nginx
# Restrict cache purging
location ~ /purge(/.*) {
    allow 127.0.0.1;
    allow 192.168.1.0/24;
    deny all;
    
    proxy_cache_purge my_cache $scheme$proxy_host$1;
}

# Don't cache sensitive data
location /api/auth/ {
    proxy_pass http://backend;
    proxy_no_cache 1;
    proxy_cache_bypass 1;
}
```

### 4. Performance Optimization
```nginx
# Use appropriate cache levels
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;

# Enable background updates
proxy_cache_background_update on;
proxy_cache_use_stale updating;

# Optimize cache validation
proxy_cache_valid 200 302 10m;
proxy_cache_valid 404 1m;
```

## Docker Setup

### 1. Basic Docker Configuration
```dockerfile
# Dockerfile
FROM nginx:alpine

# Copy custom configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Create cache directory
RUN mkdir -p /var/cache/nginx

# Expose ports
EXPOSE 80 443
```

### 2. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    build: .
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./conf.d:/etc/nginx/conf.d
      - nginx_cache:/var/cache/nginx
      - nginx_logs:/var/log/nginx
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    image: myapp:latest
    ports:
      - "8000:8000"
    restart: unless-stopped

volumes:
  nginx_cache:
  nginx_logs:
```

### 3. Nginx Configuration for Docker
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Cache configuration
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
    
    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    include /etc/nginx/conf.d/*.conf;
}
```

## Practical Examples

### 1. API Caching
```nginx
# API endpoint caching
location /api/ {
    proxy_pass http://backend:8000;
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_cache_valid 404 1m;
    proxy_cache_key $scheme$proxy_host$request_uri$args;
    
    # Cache headers
    add_header X-Cache-Status $upstream_cache_status;
    
    # Don't cache POST requests
    proxy_cache_bypass $request_method;
    proxy_no_cache $request_method;
}
```

### 2. Static File Caching
```nginx
# Static files with long cache
location /static/ {
    alias /var/www/static/;
    expires 1y;
    add_header Cache-Control "public, immutable";
    
    # Gzip compression
    gzip_static on;
}
```

### 3. Microservices Caching
```nginx
# Different cache rules for different services
upstream user_service {
    server user-service:8000;
}

upstream product_service {
    server product-service:8000;
}

server {
    # User service caching
    location /api/users/ {
        proxy_pass http://user_service;
        proxy_cache user_cache;
        proxy_cache_valid 200 2m;  # User data changes frequently
    }
    
    # Product service caching
    location /api/products/ {
        proxy_pass http://product_service;
        proxy_cache product_cache;
        proxy_cache_valid 200 30m;  # Products change less frequently
    }
}
```

### 4. E-commerce Caching Strategy
```nginx
# E-commerce site caching
server {
    # Product pages - cache for 1 hour
    location /products/ {
        proxy_pass http://backend;
        proxy_cache product_cache;
        proxy_cache_valid 200 1h;
        proxy_cache_key $scheme$proxy_host$request_uri;
    }
    
    # Shopping cart - no caching
    location /cart/ {
        proxy_pass http://backend;
        proxy_no_cache 1;
        proxy_cache_bypass 1;
    }
    
    # User profile - no caching
    location /profile/ {
        proxy_pass http://backend;
        proxy_no_cache 1;
        proxy_cache_bypass 1;
    }
    
    # Search results - cache for 5 minutes
    location /search/ {
        proxy_pass http://backend;
        proxy_cache search_cache;
        proxy_cache_valid 200 5m;
        proxy_cache_key $scheme$proxy_host$request_uri$args;
    }
}
```

## Conclusion

Nginx caching is a powerful tool for improving web application performance. Key points:

### **What is Nginx?**
- High-performance web server and reverse proxy
- Handles thousands of concurrent connections
- Low memory usage with event-driven architecture

### **What is Nginx Cache?**
- Stores HTTP responses from backend servers
- Serves cached content directly without backend requests
- Improves response times and reduces server load

### **Why Use Nginx Cache?**
- **Performance**: Faster response times
- **Cost**: Reduced backend server requirements
- **Scalability**: Handle traffic spikes
- **User Experience**: Lower latency

### **When to Use**
- ✅ Static content, API responses, database queries
- ❌ User-specific content, real-time data, sensitive information

### **Best Practices**
- Design appropriate cache keys
- Set proper cache expiration times
- Monitor cache hit ratios
- Implement cache invalidation strategies
- Use security measures for cache purging

Nginx caching is essential for building high-performance, scalable web applications!
