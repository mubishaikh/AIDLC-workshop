# Unit 1: Idea Submission & Management - Logical Components

## Overview
This document defines the logical infrastructure components required to implement NFR requirements for Unit 1. These components work together to provide performance, scalability, security, and reliability.

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  (Web Browser, Mobile App)                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  Load Balancer Layer                             │
│  (Nginx)                                                         │
│  - SSL/TLS termination                                           │
│  - Request routing                                               │
│  - Rate limiting                                                 │
│  - Reverse proxy                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              Application Layer (Stateless)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  API Pod 1   │  │  API Pod 2   │  │  API Pod 3   │           │
│  │  (Django/    │  │  (Django/    │  │  (Django/    │           │
│  │  FastAPI)    │  │  FastAPI)    │  │  FastAPI)    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  - Request validation                                            │
│  - Business logic                                                │
│  - Authentication/Authorization                                  │
│  - Static asset serving                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼──────────┐ ┌──▼──────────────┐
│  Cache Layer   │ │  Queue Layer  │ │  Storage Layer │
│  (Redis)       │ │  (SQS/Celery) │ │  (S3/Blob)     │
└───────┬────────┘ └────┬──────────┘ └──┬──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼──────────┐ ┌──▼──────────────┐
│  Database      │ │  Background   │ │  External       │
│  (PostgreSQL)  │ │  Workers      │ │  Services       │
│                │ │  (Celery)     │ │  (Virus Scan)   │
└────────────────┘ └───────────────┘ └─────────────────┘
        │
┌───────▼────────────────────────────────────────────┐
│         Monitoring & Observability                 │
│  - Prometheus (metrics)                            │
│  - Jaeger (tracing)                                │
│  - ELK Stack (logging)                             │
│  - Grafana (dashboards)                            │
│  - AlertManager (alerts)                           │
└────────────────────────────────────────────────────┘
```

---

## 1. Client Layer

### Component: Web Browser / Mobile App

**Purpose**: User interface for idea submission and management

**Responsibilities**:
- Render UI components
- Collect user input
- Validate input (client-side)
- Display ideas and status
- Handle authentication

**Technology**:
- React 18+ (web)
- React Native or Flutter (mobile)
- Material-UI or Ant Design (components)

**Performance Considerations**:
- Lazy load components
- Code splitting
- Image optimization
- Service workers for offline support

---

## 2. Load Balancer Layer

### Component: Nginx Reverse Proxy

**Purpose**: Route requests, enforce security, manage traffic

**Responsibilities**:
- SSL/TLS termination
- Request routing to API instances
- Rate limiting
- Reverse proxy
- Request/response logging
- Static asset serving

**Technology**:
- Nginx 1.20+
- Docker (containerization)
- Kubernetes (orchestration)

**Configuration**:
```nginx
upstream api_backend {
    least_conn;
    server api-1:8000 max_fails=3 fail_timeout=30s;
    server api-2:8000 max_fails=3 fail_timeout=30s;
    server api-3:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 443 ssl http2;
    server_name ideation.example.com;
    
    # SSL/TLS Configuration
    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
    limit_req_zone $http_x_forwarded_for zone=user_limit:10m rate=10r/s;
    
    # Static Assets
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API Endpoints
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_req zone=user_limit burst=5 nodelay;
        
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
    
    # Health Check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}

# HTTP to HTTPS Redirect
server {
    listen 80;
    server_name ideation.example.com;
    return 301 https://$server_name$request_uri;
}
```

**Deployment**:
- Docker container
- Kubernetes deployment (2-3 replicas for HA)
- Configuration via ConfigMap

**Health Checks**:
- Endpoint: /health
- Interval: 30 seconds
- Timeout: 5 seconds
- Unhealthy threshold: 3 failures

**Performance Impact**:
- Distributes load across instances
- Enables auto-scaling
- Provides high availability
- Reduces latency with connection pooling

---

## 3. Application Layer

### Component: API Instances (Stateless)

**Purpose**: Process requests and execute business logic

**Responsibilities**:
- Validate requests
- Authenticate users
- Authorize actions
- Execute business logic
- Return responses
- Serve static assets (React build)

**Technology**:
- Python 3.9+
- Django 4.0+ or FastAPI 0.95+
- Gunicorn (WSGI server)
- Docker (containerization)

**Configuration**:
```
Instances: 2-10 (auto-scaling)
CPU: 2 cores
Memory: 2 GB
Timeout: 30 seconds
Concurrency: 100 requests per instance
```

**Static Asset Serving**:
- Serve React build from /static/ directory
- Nginx handles caching (1 year for versioned assets)
- Fallback to index.html for SPA routing

**Deployment**:
- Docker container
- Kubernetes pod (optional)
- AWS ECS task (optional)

**Performance Considerations**:
- Connection pooling to database
- Caching frequently accessed data
- Async processing for long operations
- Request timeout handling

---

## 5. Cache Layer

### Component: Redis Cluster

**Purpose**: Cache frequently accessed data to reduce database load

**Responsibilities**:
- Cache idea lists
- Cache user profiles
- Cache campaign metadata
- Session management
- Rate limiting counters

**Technology**:
- Redis 6+
- Redis Cluster (for high availability)
- Redis Sentinel (for failover)

**Configuration**:
```
Cluster: 3 nodes (master + 2 replicas)
Memory: 4 GB per node
Eviction Policy: allkeys-lru
Persistence: AOF (Append-Only File)
Replication: Async
Backup: Daily snapshots
```

**Data Structure**:
```
String: User profiles, campaign metadata
Hash: Idea details, contributor lists
List: Idea lists (paginated)
Set: User roles, permissions
Sorted Set: Leaderboards, rankings
```

**TTL Strategy**:
```
User profiles: 1 hour
Campaign metadata: 1 hour
Idea lists: 5 minutes
Contributor lists: 5 minutes
Session data: 24 hours
Rate limit counters: 1 hour
```

**Performance Impact**:
- Reduces database queries by 80%+
- Improves response time by 50-70%
- Supports 100+ concurrent users

---

## 6. Queue Layer

### Component: Message Queue

**Purpose**: Handle asynchronous processing and decouple services

**Responsibilities**:
- Queue idea submissions
- Queue file uploads
- Queue virus scans
- Queue notifications
- Retry failed jobs

**Technology**:
- AWS SQS (managed)
- Celery + Redis (self-hosted)
- RabbitMQ (self-hosted)

**Configuration**:
```
Queue: ideation-submissions
Workers: 5-10 (auto-scaling)
Batch Size: 10 messages
Visibility Timeout: 300 seconds
Retry Policy: Exponential backoff (1s, 2s, 4s, 8s)
Dead Letter Queue: ideation-submissions-dlq
```

**Job Types**:
```
1. submit_idea: Process idea submission
2. upload_file: Process file upload
3. scan_virus: Scan uploaded file
4. send_notification: Send user notification
5. generate_report: Generate analytics report
```

**Performance Impact**:
- Handles submission spikes gracefully
- Prevents API overload
- Enables parallel processing

---

## 7. Storage Layer

### Component: File Storage

**Purpose**: Store uploaded documents and files

**Responsibilities**:
- Store idea documents
- Store contributor attachments
- Manage file access
- Enforce retention policies

**Technology**:
- AWS S3
- Azure Blob Storage
- Google Cloud Storage

**Configuration**:
```
Bucket: ideation-documents
Encryption: AES-256 (server-side)
Versioning: Enabled
Access Control: Private (default)
Lifecycle Policy:
  - Delete old versions after 30 days
  - Archive to Glacier after 90 days
  - Delete after 1 year
Backup: Cross-region replication
```

**Security**:
- Bucket policy: Deny public access
- Encryption: AES-256
- Access logging: Enabled
- Virus scanning: Pre-upload

**Performance Impact**:
- Offloads file storage from database
- Enables large file uploads
- Provides high availability

---

## 8. Database Layer

### Component: PostgreSQL Database

**Purpose**: Store persistent data

**Responsibilities**:
- Store ideas, drafts, contributors
- Store user data
- Store campaign data
- Maintain data consistency
- Provide query performance

**Technology**:
- PostgreSQL 12+
- AWS RDS (managed)
- Azure Database for PostgreSQL (managed)

**Configuration**:
```
Instance: db.r5.xlarge (4 vCPU, 32 GB RAM)
Storage: 500 GB (gp3)
Backup: Daily automated backups (30-day retention)
Replication: Multi-AZ (automatic failover)
Encryption: AES-256 (at-rest)
SSL: TLS 1.2+ (in-transit)
```

**Indexes**:
```
Primary: ideas(id)
Composite: ideas(submitter_id, status)
Composite: ideas(campaign_id, status)
Full-text: ideas(title, description)
Partial: ideas(submitter_id) WHERE status='DRAFT'
```

**Performance Tuning**:
- Connection pooling (PgBouncer)
- Query optimization
- Index maintenance
- Vacuum and analyze

**Performance Impact**:
- Supports 10,000+ ideas
- Supports 100 concurrent users
- Query response < 100ms

---

## 9. Background Workers

### Component: Celery Workers

**Purpose**: Process asynchronous jobs

**Responsibilities**:
- Process idea submissions
- Process file uploads
- Scan files for viruses
- Send notifications
- Generate reports

**Technology**:
- Celery 5.0+
- Redis (message broker)
- Python 3.9+

**Configuration**:
```
Workers: 5-10 (auto-scaling)
Concurrency: 4 per worker
Timeout: 300 seconds
Retry: 3 attempts with exponential backoff
Dead Letter Queue: Enabled
```

**Job Types**:
```
1. submit_idea_job
   - Validate idea data
   - Create idea record
   - Add submitter as contributor
   - Update campaign stats
   - Send confirmation email

2. upload_file_job
   - Validate file
   - Scan for viruses
   - Upload to S3
   - Update database
   - Send completion notification

3. scan_virus_job
   - Download file
   - Scan with ClamAV
   - Update scan status
   - Notify user
   - Delete if infected

4. send_notification_job
   - Format notification
   - Send email
   - Log notification
   - Retry on failure
```

**Performance Impact**:
- Handles 50+ submissions/minute
- Prevents API timeout
- Enables parallel processing

---

## 10. External Services

### Component: Virus Scanning Service

**Purpose**: Scan uploaded files for malware

**Responsibilities**:
- Scan files before storage
- Detect viruses and malware
- Quarantine infected files
- Log scan results

**Technology**:
- ClamAV (open-source)
- VirusTotal API (cloud-based)

**Configuration**:
```
Service: ClamAV
Deployment: Docker container
Update: Daily virus definitions
Timeout: 10 seconds per file
Max File Size: 10 MB
```

**Integration**:
```python
def scan_file(file_path):
    try:
        result = clam_av.scan(file_path)
        if result[1] == 1:  # Virus found
            log_infection(file_path)
            raise VirusDetectedException()
        return True
    except Exception as e:
        log_error(e)
        raise
```

**Performance Impact**:
- Prevents malware upload
- Adds 5-10 seconds to upload process
- Runs asynchronously

---

## 11. Monitoring & Observability

### Component: Prometheus

**Purpose**: Collect and store metrics

**Responsibilities**:
- Collect API metrics
- Collect database metrics
- Collect cache metrics
- Store time-series data
- Enable alerting

**Technology**:
- Prometheus 2.0+
- Node Exporter (system metrics)
- PostgreSQL Exporter (database metrics)
- Redis Exporter (cache metrics)

**Configuration**:
```
Scrape Interval: 15 seconds
Retention: 15 days
Storage: 50 GB
Replication: 2 replicas
```

**Metrics**:
```
http_requests_total
http_request_duration_seconds
db_query_duration_seconds
redis_connected_clients
redis_used_memory_bytes
```

---

### Component: Grafana

**Purpose**: Visualize metrics and create dashboards

**Responsibilities**:
- Create dashboards
- Visualize metrics
- Create alerts
- Enable data exploration

**Technology**:
- Grafana 8.0+
- Prometheus data source

**Dashboards**:
```
1. System Health
   - CPU, memory, disk usage
   - Network I/O
   - Container status

2. API Performance
   - Request rate
   - Response time (p50, p95, p99)
   - Error rate
   - Throughput

3. Database Performance
   - Query time
   - Connection count
   - Cache hit rate
   - Replication lag

4. Business Metrics
   - Ideas submitted
   - Ideas by status
   - Average submission time
   - Top contributors
```

---

### Component: Jaeger

**Purpose**: Distributed tracing for debugging

**Responsibilities**:
- Trace requests across services
- Identify performance bottlenecks
- Debug complex issues
- Analyze latency

**Technology**:
- Jaeger 1.0+
- Elasticsearch (storage)

**Configuration**:
```
Sampling: 100% (for development), 10% (for production)
Storage: Elasticsearch
Retention: 72 hours
```

---

### Component: ELK Stack

**Purpose**: Centralized logging and analysis

**Responsibilities**:
- Collect logs from all components
- Index and store logs
- Enable log search and analysis
- Create alerts

**Technology**:
- Elasticsearch 7.0+
- Logstash 7.0+
- Kibana 7.0+

**Configuration**:
```
Elasticsearch: 3 nodes, 100 GB storage
Logstash: 2 instances
Kibana: 1 instance
Retention: 30 days
```

**Log Types**:
```
1. Application logs
   - Request/response
   - Business logic
   - Errors and exceptions

2. Database logs
   - Slow queries
   - Connection errors
   - Replication issues

3. Infrastructure logs
   - Container logs
   - System logs
   - Network logs
```

---

### Component: AlertManager

**Purpose**: Alert on anomalies and issues

**Responsibilities**:
- Evaluate alert rules
- Send notifications
- Group related alerts
- Manage alert lifecycle

**Technology**:
- Prometheus AlertManager
- Slack, PagerDuty, Email

**Alert Rules**:
```
1. HighErrorRate
   - Condition: Error rate > 5%
   - Duration: 5 minutes
   - Action: Notify on-call engineer

2. SlowAPIResponse
   - Condition: p95 response time > 1 second
   - Duration: 5 minutes
   - Action: Notify team

3. HighDatabaseConnections
   - Condition: Active connections > 80
   - Duration: 5 minutes
   - Action: Notify DBA

4. LowCacheHitRate
   - Condition: Cache hit rate < 70%
   - Duration: 10 minutes
   - Action: Notify team
```

---

## Component Interactions

### Idea Submission Flow

```
1. User submits idea via web UI
   ↓
2. Request → API Gateway (rate limit, validate)
   ↓
3. API Instance (authenticate, validate input)
   ↓
4. Check Redis cache for campaign data
   ↓
5. Queue submission job (SQS/Celery)
   ↓
6. Return 202 Accepted to user
   ↓
7. Background worker processes job
   ↓
8. Create idea in PostgreSQL
   ↓
9. Add submitter as contributor
   ↓
10. Update campaign stats
   ↓
11. Invalidate Redis cache
   ↓
12. Send notification to user
   ↓
13. Log event to ELK Stack
   ↓
14. Emit metrics to Prometheus
```

### File Upload Flow

```
1. User uploads file via web UI
   ↓
2. Request → API Gateway (rate limit)
   ↓
3. API Instance (validate file)
   ↓
4. Upload to temporary S3 location
   ↓
5. Return 202 Accepted with upload ID
   ↓
6. Queue virus scan job
   ↓
7. Background worker scans file
   ↓
8. If clean: Move to permanent S3 location
   ↓
9. Update database with file metadata
   ↓
10. Send completion notification
   ↓
11. If infected: Quarantine and notify user
```

---

## Deployment Architecture

### Development Environment
```
Docker Compose:
- Nginx (load balancer)
- API (1 instance)
- PostgreSQL (1 instance)
- Redis (1 instance)
- Celery worker (1 instance)
- Prometheus (1 instance)
- Grafana (1 instance)
```

### Staging Environment
```
Kubernetes:
- Nginx (2 replicas)
- API (3 replicas)
- PostgreSQL (1 instance with backup)
- Redis (3 nodes)
- Celery workers (3 replicas)
- Prometheus (1 instance)
- Grafana (1 instance)
- Jaeger (1 instance)
- ELK Stack (3 nodes)
```

### Production Environment
```
Kubernetes:
- Nginx (3-5 replicas, auto-scaling)
- API (5-10 replicas, auto-scaling)
- PostgreSQL (Multi-AZ with failover)
- Redis Cluster (3 nodes)
- Celery workers (5-10 replicas, auto-scaling)
- Prometheus (2 instances, HA)
- Grafana (2 instances, HA)
- Jaeger (3 instances, HA)
- ELK Stack (5+ nodes, HA)
```

---

## Summary

**Total Logical Components**: 10 major components

**Load Balancing Component**:
- Nginx reverse proxy with SSL/TLS termination, rate limiting, and static asset serving

**Performance Components**:
- Nginx static asset serving (React build)
- Redis (caching)
- Database indexes (query optimization)

**Scalability Components**:
- Nginx load balancing (traffic distribution)
- Auto-scaling (dynamic capacity)
- Message queue (async processing)

**Security Components**:
- Nginx rate limiting and reverse proxy
- Encryption (transit, at-rest)
- Virus scanning (malware detection)

**Reliability Components**:
- Database replication (failover)
- Redis cluster (high availability)
- Background workers (async processing)

**Observability Components**:
- Prometheus (metrics)
- Grafana (dashboards)
- Jaeger (tracing)
- ELK Stack (logging)
- AlertManager (alerting)

**Total Infrastructure**: 18+ services for complete solution

