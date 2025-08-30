# CDN (Content Delivery Network) / CDN Cache

## What is CDN?

**CDN** is a distributed network of servers located in different geographic locations that delivers content to users from the server closest to them.

## Main CDN Components:

1. **Edge servers** - servers located close to users
2. **Origin server** - main server with original content
3. **CDN provider** - company providing CDN services (Cloudflare, AWS CloudFront, Akamai)

## When and Why to Use CDN:

### When to use:
- **Geographically distributed audience** - users in different countries/regions
- **High traffic** - many concurrent users
- **Static content** - images, CSS, JS, videos, documents
- **Slow loading** - website performance issues
- **High availability requirements** - mission-critical applications

### Why use CDN:

#### 1. Loading speed:
- Content delivered from nearest server
- Reduced latency (response time)
- Improved user experience

#### 2. Reduced load on main server:
- Static content caching
- Origin server offloading
- Bandwidth savings

#### 3. Increased reliability:
- Load distribution
- DDoS attack protection
- Automatic failover

#### 4. Global availability:
- Content available 24/7
- Operation across different time zones
- Scalability

## Content Types for CDN:

- **Static files:** CSS, JavaScript, images
- **Media content:** videos, audio, documents
- **API responses:** cacheable data
- **Web pages:** static HTML pages

## Popular CDN Providers:

### Free/Affordable:
- **Cloudflare** - free plan, good DDoS protection
- **jsDelivr** - free CDN for open source projects
- **unpkg** - CDN for npm packages

### Enterprise solutions:
- **AWS CloudFront** - integration with AWS ecosystem
- **Akamai** - enterprise solutions, high performance
- **Google Cloud CDN** - integration with GCP
- **Azure CDN** - integration with Microsoft Azure
- **KeyCDN** - affordable alternative provider

## CDN Setup:

### 1. Provider selection
```bash
# Cloudflare setup example
# 1. Register at cloudflare.com
# 2. Add domain
# 3. Change DNS records
# 4. Configure caching
```

### 2. Caching configuration
```nginx
# Nginx configuration example for CDN work
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary Accept-Encoding;
}
```

### 3. CORS setup (if needed)
```nginx
# CORS permission for static resources
location /static/ {
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
    add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range";
}
```

## Monitoring and Optimization:

### Metrics to track:
- **Cache Hit Ratio** - percentage of requests served from cache
- **Latency** - response time
- **Bandwidth** - amount of data transferred
- **Error Rate** - percentage of errors

### Monitoring tools:
- **Google PageSpeed Insights**
- **GTmetrix**
- **WebPageTest**
- **CDN providers** offer their own dashboards

## Best Practices:

1. **Static caching** - configure long-term caching for static resources
2. **Compression** - use gzip/brotli compression
3. **HTTP/2** - enable HTTP/2 support
4. **SSL/TLS** - use HTTPS for all resources
5. **Monitoring** - track performance and errors
6. **Fallback** - configure fallback to origin server when CDN is unavailable

## Usage Examples:

### For web applications:
```html
<!-- Connecting libraries via CDN -->
<script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
```

### For API:
```python
# Caching setup example in FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
async def get_data():
    # API endpoint with caching
    return {"data": "cached_response"}
```

CDN is especially important for web applications with international audiences and high performance requirements.
