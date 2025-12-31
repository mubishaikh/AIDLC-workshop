# Unit 1: Idea Submission & Management - NFR Design Patterns

## Overview
This document defines the design patterns used to implement NFR requirements for Unit 1. Each pattern addresses specific performance, scalability, security, and reliability requirements.

---

## 1. Performance Patterns

### Pattern 1.1: Multi-Level Caching Strategy

**Requirement**: Cache hit rate > 80% for idea lists, < 1 second response time

**Pattern**: Layered Cache (Redis + In-Memory)

**Implementation**:
```
Request → In-Memory Cache (L1) → Redis Cache (L2) → Database (L3)
```

**Details**:
- **L1 Cache (In-Memory)**: Application-level cache for frequently accessed data
  - TTL: 1 minute
  - Size: 100 MB max
  - Data: User profiles, campaign metadata
  - Invalidation: On update, with cache key versioning

- **L2 Cache (Redis)**: Distributed cache for shared data
  - TTL: 5 minutes for idea lists, 1 hour for user data
  - Data: Idea lists, contributor lists, campaign data
  - Invalidation: Event-driven (publish/subscribe)
  - Replication: Master-slave for high availability

- **L3 (Database)**: Source of truth
  - PostgreSQL with query optimization
  - Indexes on frequently queried columns

**Cache Keys**:
```
ideas:campaign:{campaignId}:page:{page}
ideas:user:{userId}:status:{status}
user:profile:{userId}
campaign:metadata:{campaignId}
```

**Invalidation Strategy**:
- On idea submission: Invalidate campaign idea list cache
- On idea update: Invalidate specific idea cache + campaign list
- On contributor add: Invalidate idea cache
- Eventual consistency: 5-minute TTL ensures eventual consistency

**Benefits**:
- Reduces database load by 80%+
- Improves response time to < 500ms
- Supports 100+ concurrent users

---

### Pattern 1.2: Database Query Optimization

**Requirement**: Get My Ideas query < 100ms for 1000 ideas

**Pattern**: Indexed Queries + Query Optimization

**Implementation**:

**Indexes**:
```sql
-- Composite indexes for common queries
CREATE INDEX idx_ideas_submitter_status ON ideas(submitter_id, status);
CREATE INDEX idx_ideas_campaign_status ON ideas(campaign_id, status);
CREATE INDEX idx_ideas_created_at ON ideas(created_at DESC);
CREATE INDEX idx_ideas_title_search ON ideas USING GIN(to_tsvector('english', title));
CREATE INDEX idx_ideas_description_search ON ideas USING GIN(to_tsvector('english', description));

-- Partial indexes for common filters
CREATE INDEX idx_ideas_draft ON ideas(submitter_id) WHERE status = 'DRAFT';
CREATE INDEX idx_ideas_submitted ON ideas(campaign_id) WHERE status IN ('SUBMITTED', 'UNDER_EVALUATION');
```

**Query Optimization**:
- Use SELECT specific columns (not SELECT *)
- Use LIMIT and OFFSET for pagination
- Use JOIN instead of N+1 queries
- Use database views for complex aggregations

**Example Optimized Query**:
```sql
SELECT id, title, status, created_at, expected_impact
FROM ideas
WHERE submitter_id = $1 AND campaign_id = $2
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;
```

**Performance Target**: < 100ms for 1000 ideas

---

### Pattern 1.3: Asynchronous File Processing

**Requirement**: File upload < 5 seconds, virus scan < 10 seconds

**Pattern**: Async Upload with Background Processing

**Implementation**:
```
User Upload → API (return 202) → Queue → Background Worker → S3 + Virus Scan
```

**Details**:
- **Synchronous**: Upload file to temporary storage, return upload ID
- **Asynchronous**: Background worker processes file
  - Virus scan using ClamAV
  - Move to permanent S3 storage
  - Update database with file status
  - Notify user of completion

**Flow**:
1. User uploads file (< 2 seconds)
2. API returns 202 Accepted with upload ID
3. Background worker processes file (< 10 seconds)
4. User polls or receives webhook notification

**Benefits**:
- Responsive user experience
- Prevents timeout on large files
- Allows parallel processing

---

## 2. Scalability Patterns

### Pattern 2.1: Nginx Load Balancing with Rate Limiting

**Requirement**: Support 100 concurrent users, 50 submissions/minute

**Pattern**: Nginx Reverse Proxy with Least Connections

**Implementation**:
```
Nginx Load Balancer → API Instance 1
                   → API Instance 2
                   → API Instance 3
                   ↓
                PostgreSQL (Primary)
                Redis (Shared)
                S3 (Shared)
```

**Details**:
- **Stateless Design**: No session state in API instances
  - Use JWT tokens for authentication
  - Store session data in Redis
  - Use database for persistent data

- **Nginx Configuration**: Least connections algorithm
  - Round-robin with health checks
  - Connection draining on shutdown
  - Rate limiting per IP and per user

- **Auto-Scaling**: Scale based on metrics
  - CPU > 70%: Add instance
  - CPU < 30%: Remove instance
  - Min instances: 2, Max instances: 10

**Nginx Configuration**:
```nginx
upstream api_backend {
    least_conn;
    server api-1:8000 max_fails=3 fail_timeout=30s;
    server api-2:8000 max_fails=3 fail_timeout=30s;
    server api-3:8000 max_fails=3 fail_timeout=30s;
}

limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
limit_req_zone $http_x_forwarded_for zone=user_limit:10m rate=10r/s;

server {
    listen 443 ssl http2;
    
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_req zone=user_limit burst=5 nodelay;
        proxy_pass http://api_backend;
    }
}
```

**Benefits**:
- Supports 100+ concurrent users
- No single point of failure
- Easy to scale up/down
- Built-in rate limiting

---

### Pattern 2.2: Database Connection Pooling

**Requirement**: Support 100 concurrent users with efficient database connections

**Pattern**: Connection Pool with PgBouncer

**Implementation**:
```
API Instances → PgBouncer (Connection Pool) → PostgreSQL
```

**Details**:
- **PgBouncer**: Lightweight connection pooler
  - Pool size: 100 connections
  - Reserve pool: 10 connections
  - Timeout: 600 seconds
  - Mode: Transaction pooling

- **Configuration**:
```
[databases]
ideation_db = host=postgres.rds.amazonaws.com port=5432 dbname=ideation

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
reserve_pool_size = 5
reserve_pool_timeout = 3
```

**Benefits**:
- Reduces database connection overhead
- Supports more concurrent users
- Improves database performance

---

### Pattern 2.3: Request Queuing for Submission Spikes

**Requirement**: Handle 50 submissions/minute with graceful degradation

**Pattern**: Message Queue with Background Workers

**Implementation**:
```
User Submission → API (validate) → Queue (SQS/Celery) → Worker → Database
```

**Details**:
- **Synchronous**: Validate input, return 202 Accepted
- **Asynchronous**: Queue submission for processing
  - Workers process submissions in parallel
  - Retry on failure with exponential backoff
  - Dead letter queue for failed submissions

- **Queue Configuration**:
  - Queue: AWS SQS or Celery with Redis
  - Workers: 5-10 workers (auto-scale)
  - Batch size: 10 messages per worker
  - Visibility timeout: 300 seconds

**Benefits**:
- Handles submission spikes gracefully
- Prevents API overload
- Enables parallel processing

---

## 3. Security Patterns

### Pattern 3.1: Encryption Strategy

**Requirement**: TLS 1.2+ for transit, AES-256 for at-rest

**Pattern**: Multi-Layer Encryption

**Implementation**:

**In Transit**:
- TLS 1.2+ for all API endpoints
- HTTPS only (redirect HTTP to HTTPS)
- Certificate: AWS Certificate Manager (auto-renewal)
- HSTS header: max-age=31536000

**At Rest**:
- Database encryption: AWS RDS encryption (AES-256)
- File storage: AWS S3 encryption (AES-256)
- Secrets: AWS Secrets Manager (encrypted)

**Field-Level Encryption** (for GDPR compliance):
- Encrypt sensitive fields at application level
- Fields: Idea description, contributor notes
- Algorithm: AES-256-GCM
- Key management: AWS KMS

**Implementation**:
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class FieldEncryption:
    def __init__(self, kms_key_id):
        self.kms_key_id = kms_key_id
    
    def encrypt(self, plaintext):
        # Get key from AWS KMS
        key = self.get_kms_key()
        cipher = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, plaintext.encode(), None)
        return nonce + ciphertext
    
    def decrypt(self, ciphertext):
        # Get key from AWS KMS
        key = self.get_kms_key()
        cipher = AESGCM(key)
        nonce = ciphertext[:12]
        plaintext = cipher.decrypt(nonce, ciphertext[12:], None)
        return plaintext.decode()
```

**Benefits**:
- Protects data in transit and at rest
- Complies with GDPR requirements
- Enables secure key management

---

### Pattern 3.2: Rate Limiting & DDoS Protection

**Requirement**: Limit submissions (10/hour), API calls (1000/hour), failed logins (5/15min)

**Pattern**: Token Bucket Algorithm with Redis

**Implementation**:
```
Request → Rate Limiter (Redis) → Check Quota → Allow/Reject
```

**Details**:
- **Token Bucket Algorithm**:
  - Each user has a bucket with tokens
  - Tokens refill at fixed rate
  - Request consumes 1 token
  - No tokens = request rejected

- **Rate Limits**:
```
submissions: 10 per hour per user
api_calls: 1000 per hour per user
failed_logins: 5 per 15 minutes per IP
```

- **Implementation**:
```python
import redis
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key, limit, window_seconds):
        current = self.redis.incr(key)
        if current == 1:
            self.redis.expire(key, window_seconds)
        return current <= limit
    
    def check_submission_limit(self, user_id):
        key = f"submissions:{user_id}:{datetime.now().hour}"
        return self.is_allowed(key, 10, 3600)
    
    def check_api_limit(self, user_id):
        key = f"api_calls:{user_id}:{datetime.now().hour}"
        return self.is_allowed(key, 1000, 3600)
    
    def check_login_limit(self, ip_address):
        key = f"failed_logins:{ip_address}:{datetime.now().minute // 15}"
        return self.is_allowed(key, 5, 900)
```

- **DDoS Protection**:
  - AWS WAF for IP-based blocking
  - CloudFlare for DDoS mitigation
  - Rate limiting at API gateway level

**Benefits**:
- Prevents abuse and DoS attacks
- Protects API from overload
- Enables fair resource allocation

---

### Pattern 3.3: Input Validation & Sanitization

**Requirement**: Prevent SQL injection, XSS, and other attacks

**Pattern**: Layered Validation

**Implementation**:

**Backend Validation**:
```python
from pydantic import BaseModel, validator
import bleach

class IdeaSubmissionRequest(BaseModel):
    title: str
    description: str
    expected_impact: str
    
    @validator('title')
    def validate_title(cls, v):
        if not v or len(v) > 200:
            raise ValueError('Title must be 1-200 characters')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if not v or len(v) > 2000:
            raise ValueError('Description must be 1-2000 characters')
        # Sanitize HTML
        return bleach.clean(v, tags=['b', 'i', 'u', 'p', 'br'], strip=True)
    
    @validator('expected_impact')
    def validate_impact(cls, v):
        if v not in ['HIGH', 'MEDIUM', 'LOW']:
            raise ValueError('Invalid impact level')
        return v
```

**Frontend Validation**:
- Client-side validation for UX
- Server-side validation for security
- Never trust client input

**SQL Injection Prevention**:
- Use parameterized queries (ORM)
- Never concatenate SQL strings
- Use prepared statements

**XSS Prevention**:
- Sanitize user input
- Escape output in templates
- Use Content Security Policy (CSP) headers

**Benefits**:
- Prevents common attacks
- Ensures data quality
- Protects user data

---

## 4. Resilience Patterns

### Pattern 4.1: Error Handling & Retry Strategy

**Requirement**: Graceful error handling, meaningful error messages

**Pattern**: Exponential Backoff with Circuit Breaker

**Implementation**:

**Exponential Backoff**:
```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, base_delay=1)
def call_external_service():
    # Call external service with retry
    pass
```

**Circuit Breaker Pattern**:
```python
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

**Error Response Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title must be 1-200 characters",
    "details": {
      "field": "title",
      "constraint": "length"
    }
  }
}
```

**Benefits**:
- Handles transient failures gracefully
- Prevents cascading failures
- Provides meaningful error messages

---

### Pattern 4.2: Data Consistency & Transactions

**Requirement**: Data consistency for multi-step operations

**Pattern**: Database Transactions with Optimistic Locking

**Implementation**:

**Database Transactions**:
```python
from django.db import transaction

@transaction.atomic
def submit_idea(user_id, campaign_id, title, description):
    # All operations succeed or all fail
    idea = Idea.objects.create(
        submitter_id=user_id,
        campaign_id=campaign_id,
        title=title,
        description=description,
        status='SUBMITTED'
    )
    
    # Add submitter as contributor
    Contributor.objects.create(
        idea_id=idea.id,
        user_id=user_id,
        role='SUBMITTER'
    )
    
    # Update campaign stats
    campaign = Campaign.objects.select_for_update().get(id=campaign_id)
    campaign.idea_count += 1
    campaign.save()
    
    return idea
```

**Optimistic Locking**:
```python
class Idea(models.Model):
    # ... other fields ...
    version = models.IntegerField(default=1)
    
    def update_with_locking(self, **kwargs):
        current_version = self.version
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.version += 1
        
        # Update only if version hasn't changed
        updated = Idea.objects.filter(
            id=self.id,
            version=current_version
        ).update(**{**kwargs, 'version': self.version})
        
        if updated == 0:
            raise ConcurrentModificationError("Idea was modified by another user")
```

**Benefits**:
- Ensures data consistency
- Prevents race conditions
- Enables concurrent updates

---

## 5. Monitoring & Observability Patterns

### Pattern 5.1: Metrics Collection & Alerting

**Requirement**: Monitor CPU, memory, API response times, error rates

**Pattern**: Prometheus + Grafana + AlertManager

**Implementation**:

**Metrics to Collect**:
```
# API Metrics
http_requests_total{method, endpoint, status}
http_request_duration_seconds{method, endpoint}
http_request_size_bytes{method, endpoint}
http_response_size_bytes{method, endpoint}

# Database Metrics
db_query_duration_seconds{query_type}
db_connection_pool_size
db_active_connections

# Business Metrics
ideas_submitted_total
ideas_by_status{status}
average_submission_time_seconds
```

**Prometheus Configuration**:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ideation-api'
    static_configs:
      - targets: ['localhost:8000']
  
  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']
  
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']
```

**Alert Rules**:
```yaml
groups:
  - name: ideation_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
      
      - alert: SlowAPIResponse
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 5m
        annotations:
          summary: "API response time is slow"
      
      - alert: HighDatabaseConnections
        expr: db_active_connections > 80
        for: 5m
        annotations:
          summary: "High database connection usage"
```

**Benefits**:
- Real-time visibility into system health
- Proactive issue detection
- Data-driven optimization

---

### Pattern 5.2: Distributed Tracing

**Requirement**: Debug issues across multiple services

**Pattern**: Distributed Tracing with Jaeger

**Implementation**:

**Trace Context Propagation**:
```python
from jaeger_client import Config
from opentracing_instrumentation.local_span import get_current_span

def create_tracer():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='ideation-api',
    )
    return config.initialize_tracer()

@app.route('/ideas', methods=['POST'])
def submit_idea():
    span = get_current_span()
    span.set_tag('user_id', user_id)
    span.set_tag('campaign_id', campaign_id)
    
    # Trace database call
    with tracer.start_active_span('db.create_idea'):
        idea = Idea.objects.create(...)
    
    # Trace external service call
    with tracer.start_active_span('virus_scan'):
        scan_result = virus_scanner.scan(file)
    
    return idea
```

**Benefits**:
- Trace requests across services
- Identify performance bottlenecks
- Debug complex issues

---

### Pattern 5.3: Structured Logging

**Requirement**: Comprehensive logging for debugging and compliance

**Pattern**: JSON Structured Logging

**Implementation**:

**Logging Configuration**:
```python
import logging
import json
from pythonjsonlogger import jsonlogger

# Create logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Log with context
logger.info('Idea submitted', extra={
    'user_id': user_id,
    'campaign_id': campaign_id,
    'idea_id': idea_id,
    'timestamp': datetime.now().isoformat(),
    'action': 'idea_submission',
    'status': 'success'
})

logger.error('Virus scan failed', extra={
    'file_id': file_id,
    'error': str(e),
    'timestamp': datetime.now().isoformat(),
    'action': 'virus_scan',
    'status': 'failure'
})
```

**Log Aggregation**:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- CloudWatch (AWS)
- Datadog

**Benefits**:
- Structured, queryable logs
- Easy debugging and analysis
- Compliance and audit trail

---

## Summary

**Performance Patterns**:
- Multi-level caching (L1 in-memory, L2 Redis, L3 database)
- Indexed queries with optimization
- Asynchronous file processing

**Scalability Patterns**:
- Nginx load balancing with least connections
- Database connection pooling
- Request queuing for spikes

**Security Patterns**:
- Multi-layer encryption (transit, at-rest, field-level)
- Rate limiting with token bucket algorithm
- Input validation and sanitization

**Resilience Patterns**:
- Exponential backoff with circuit breaker
- Database transactions with optimistic locking
- Graceful error handling

**Observability Patterns**:
- Prometheus + Grafana for metrics
- Jaeger for distributed tracing
- JSON structured logging

**Total Patterns**: 13 design patterns addressing all NFR categories

