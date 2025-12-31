# Unit 1: Idea Submission & Management - Infrastructure Design

## Overview
This document defines the infrastructure architecture for Unit 1, including cloud resources, networking, storage, and deployment configuration.

---

## 1. Infrastructure Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Internet                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    Nginx Load Balancer                           │
│  (Port 443 - HTTPS, Port 80 - HTTP Redirect)                    │
│  - SSL/TLS Termination                                           │
│  - Rate Limiting                                                 │
│  - Static Asset Serving                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼──────────┐ ┌──▼──────────────┐
│  API Pod 1     │ │  API Pod 2    │ │  API Pod 3      │
│  (Django/      │ │  (Django/     │ │  (Django/       │
│  FastAPI)      │ │  FastAPI)     │ │  FastAPI)       │
│  Port 8000     │ │  Port 8000    │ │  Port 8000      │
└───────┬────────┘ └────┬──────────┘ └──┬──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼──────────┐ ┌──▼──────────────┐
│  PostgreSQL    │ │  Redis        │ │  S3 Storage    │
│  Primary       │ │  Cluster      │ │  (Documents)   │
│  (Port 5432)   │ │  (Port 6379)  │ │                │
└───────┬────────┘ └────┬──────────┘ └──┬──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼──────────┐ ┌──▼──────────────┐
│  Celery        │ │  Message      │ │  Monitoring    │
│  Workers       │ │  Queue        │ │  Stack         │
│  (Port 5555)   │ │  (SQS/Redis)  │ │  (Prometheus)  │
└────────────────┘ └───────────────┘ └─────────────────┘
```

---

## 2. Cloud Platform Selection

### Recommended: AWS (Amazon Web Services)

**Rationale**:
- Largest ecosystem and service offerings
- Mature and stable platform
- Good pricing and cost optimization options
- Excellent documentation and community support
- Strong security and compliance features

**Alternative Options**:
- Azure: Good for Microsoft integration
- GCP: Good for data analytics and machine learning

### AWS Services Used

**Compute**:
- EC2 (Elastic Compute Cloud) for API instances
- ECS (Elastic Container Service) or EKS (Elastic Kubernetes Service) for orchestration
- Lambda (optional, for serverless functions)

**Database**:
- RDS (Relational Database Service) for PostgreSQL
- ElastiCache for Redis

**Storage**:
- S3 (Simple Storage Service) for documents
- EBS (Elastic Block Store) for persistent volumes

**Networking**:
- VPC (Virtual Private Cloud) for network isolation
- ALB (Application Load Balancer) or Nginx for load balancing
- Route 53 for DNS
- CloudFront (optional, for CDN - not used per requirements)

**Monitoring**:
- CloudWatch for logs and metrics
- SNS (Simple Notification Service) for alerts

**Security**:
- IAM (Identity and Access Management) for access control
- Secrets Manager for credential management
- KMS (Key Management Service) for encryption

---

## 3. Network Architecture

### VPC Configuration

**VPC Setup**:
```
VPC CIDR: 10.0.0.0/16

Subnets:
  Public Subnet 1: 10.0.1.0/24 (AZ-a)
    - Nginx Load Balancer
    - NAT Gateway
  
  Public Subnet 2: 10.0.2.0/24 (AZ-b)
    - Nginx Load Balancer (HA)
    - NAT Gateway (HA)
  
  Private Subnet 1: 10.0.10.0/24 (AZ-a)
    - API Instances
    - Celery Workers
  
  Private Subnet 2: 10.0.11.0/24 (AZ-b)
    - API Instances
    - Celery Workers
  
  Database Subnet 1: 10.0.20.0/24 (AZ-a)
    - PostgreSQL Primary
  
  Database Subnet 2: 10.0.21.0/24 (AZ-b)
    - PostgreSQL Replica
```

**Security Groups**:

```
1. Nginx Security Group (sg-nginx)
   Inbound:
     - Port 80 (HTTP) from 0.0.0.0/0
     - Port 443 (HTTPS) from 0.0.0.0/0
   Outbound:
     - All traffic to API Security Group

2. API Security Group (sg-api)
   Inbound:
     - Port 8000 from Nginx Security Group
     - Port 22 (SSH) from Bastion Security Group
   Outbound:
     - Port 5432 to Database Security Group
     - Port 6379 to Redis Security Group
     - Port 443 to 0.0.0.0/0 (HTTPS for external APIs)

3. Database Security Group (sg-database)
   Inbound:
     - Port 5432 from API Security Group
   Outbound:
     - None (database doesn't initiate connections)

4. Redis Security Group (sg-redis)
   Inbound:
     - Port 6379 from API Security Group
   Outbound:
     - None

5. Bastion Security Group (sg-bastion)
   Inbound:
     - Port 22 (SSH) from Admin IP
   Outbound:
     - Port 22 to API Security Group
     - Port 5432 to Database Security Group
```

**Network Flow**:
```
Internet → Nginx (Public Subnet)
        → API Instances (Private Subnet)
        → PostgreSQL (Database Subnet)
        → Redis (Private Subnet)
        → S3 (AWS Managed)
```

---

## 4. Compute Resources

### Nginx Load Balancer

**Deployment**:
- EC2 instances (t3.medium)
- Auto Scaling Group (2-3 instances)
- Elastic IP for static IP

**Configuration**:
```
Instance Type: t3.medium
vCPU: 2
Memory: 4 GB
Storage: 20 GB (gp3)
AMI: Ubuntu 20.04 LTS
```

**Installation**:
```bash
# Install Nginx
sudo apt-get update
sudo apt-get install -y nginx

# Install SSL certificates
sudo apt-get install -y certbot python3-certbot-nginx

# Configure Nginx (see nfr-design-patterns.md)
sudo systemctl start nginx
sudo systemctl enable nginx
```

### API Instances

**Deployment**:
- Docker containers
- ECS or EKS for orchestration
- Auto Scaling based on CPU/Memory

**Configuration**:
```
Instance Type: t3.large
vCPU: 2
Memory: 8 GB
Storage: 30 GB (gp3)
AMI: Ubuntu 20.04 LTS with Docker
```

**Docker Image**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app.wsgi"]
```

**Kubernetes Deployment** (if using EKS):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ideation-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ideation-api
  template:
    metadata:
      labels:
        app: ideation-api
    spec:
      containers:
      - name: api
        image: ideation-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Celery Workers

**Deployment**:
- Docker containers
- ECS or EKS for orchestration
- Auto Scaling based on queue depth

**Configuration**:
```
Instance Type: t3.large
vCPU: 2
Memory: 8 GB
Storage: 30 GB (gp3)
Workers: 5-10 (auto-scaling)
Concurrency: 4 per worker
```

**Docker Image**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Run Celery worker
CMD ["celery", "-A", "app.celery", "worker", "--loglevel=info", "--concurrency=4"]
```

---

## 5. Database Resources

### PostgreSQL RDS

**Configuration**:
```
Engine: PostgreSQL 12+
Instance Class: db.r5.xlarge
vCPU: 4
Memory: 32 GB
Storage: 500 GB (gp3)
Multi-AZ: Enabled (automatic failover)
Backup Retention: 30 days
Backup Window: 03:00-04:00 UTC
Maintenance Window: Sunday 04:00-05:00 UTC
```

**Database Setup**:
```sql
-- Create database
CREATE DATABASE ideation_db;

-- Create user
CREATE USER ideation_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ideation_db TO ideation_user;

-- Create schema
CREATE SCHEMA ideation;
GRANT ALL PRIVILEGES ON SCHEMA ideation TO ideation_user;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

**Connection Pooling**:
```
PgBouncer Configuration:
  Pool Size: 20
  Reserve Pool: 5
  Timeout: 600 seconds
  Mode: Transaction pooling
```

**Backup Strategy**:
- Automated daily backups (30-day retention)
- Manual snapshots before major changes
- Cross-region replication (optional)
- Point-in-time recovery enabled

**Monitoring**:
- CloudWatch metrics (CPU, memory, connections)
- Enhanced monitoring enabled
- Slow query logging enabled

---

## 6. Cache Resources

### Redis ElastiCache

**Configuration**:
```
Engine: Redis 6.0+
Node Type: cache.r6g.xlarge
Nodes: 3 (1 primary + 2 replicas)
Automatic Failover: Enabled
Multi-AZ: Enabled
Subnet Group: Private subnets
Security Group: Redis Security Group
```

**Redis Cluster Setup**:
```
Cluster Mode: Enabled
Shards: 1
Replicas per Shard: 2
Automatic Failover: Enabled
Backup Retention: 5 days
Backup Window: 03:00-04:00 UTC
```

**Data Persistence**:
```
RDB Snapshots: Daily
AOF (Append-Only File): Enabled
Backup Frequency: Daily
Retention: 5 days
```

**Monitoring**:
- CloudWatch metrics (CPU, memory, connections)
- Redis Exporter for Prometheus
- Alerts on high memory usage

---

## 7. Storage Resources

### S3 Bucket Configuration

**Bucket Setup**:
```
Bucket Name: ideation-documents-prod
Region: us-east-1
Versioning: Enabled
Server-Side Encryption: AES-256
Block Public Access: Enabled
```

**Lifecycle Policy**:
```
Rule 1: Delete old versions
  - Delete non-current versions after 30 days

Rule 2: Archive to Glacier
  - Transition to Glacier after 90 days

Rule 3: Delete archived files
  - Delete from Glacier after 1 year
```

**Access Control**:
```
Bucket Policy: Deny public access
IAM Policy: Allow API instances to read/write
Presigned URLs: For temporary access
CORS: Allow requests from ideation.example.com
```

**Monitoring**:
- CloudWatch metrics (requests, bytes)
- S3 access logging enabled
- Alerts on unusual access patterns

---

## 8. Networking & DNS

### Route 53 DNS Configuration

**DNS Records**:
```
ideation.example.com          A     → Nginx Load Balancer (EIP)
api.ideation.example.com      A     → Nginx Load Balancer (EIP)
db.ideation.example.com       CNAME → RDS Endpoint
cache.ideation.example.com    CNAME → ElastiCache Endpoint
```

**Health Checks**:
```
Primary Health Check:
  - Endpoint: ideation.example.com/health
  - Protocol: HTTPS
  - Interval: 30 seconds
  - Failure Threshold: 3
  - Alarm: SNS notification
```

### SSL/TLS Certificates

**Certificate Management**:
- AWS Certificate Manager (ACM)
- Auto-renewal enabled
- Wildcard certificate: *.ideation.example.com
- TLS 1.2+ enforcement

**Certificate Configuration**:
```
Domain: ideation.example.com
Wildcard: *.ideation.example.com
Validation: DNS
Auto-renewal: Enabled
```

---

## 9. Monitoring & Logging

### CloudWatch Configuration

**Log Groups**:
```
/ideation/nginx/access
/ideation/nginx/error
/ideation/api/application
/ideation/api/error
/ideation/celery/worker
/ideation/database/postgresql
/ideation/redis/operations
```

**Metrics**:
```
Custom Metrics:
  - http_requests_total
  - http_request_duration_seconds
  - db_query_duration_seconds
  - redis_operations_total
  - celery_task_duration_seconds
```

**Alarms**:
```
1. High CPU Usage
   - Threshold: > 70%
   - Duration: 5 minutes
   - Action: Scale up

2. High Memory Usage
   - Threshold: > 80%
   - Duration: 5 minutes
   - Action: Alert

3. High Error Rate
   - Threshold: > 5%
   - Duration: 5 minutes
   - Action: Alert

4. Database Connection Pool Exhausted
   - Threshold: > 90%
   - Duration: 2 minutes
   - Action: Alert

5. Redis Memory Usage
   - Threshold: > 85%
   - Duration: 5 minutes
   - Action: Alert
```

### Prometheus & Grafana

**Deployment**:
- EC2 instance (t3.medium)
- Docker containers
- Persistent volume for data

**Configuration**:
```
Scrape Interval: 15 seconds
Retention: 15 days
Storage: 50 GB
Replication: 2 instances (HA)
```

**Dashboards**:
- System Health (CPU, memory, disk)
- API Performance (requests, latency, errors)
- Database Performance (queries, connections)
- Business Metrics (ideas, submissions)

---

## 10. Security Configuration

### IAM Roles & Policies

**EC2 Instance Role**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::ideation-documents-prod/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:*:*:secret:ideation/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt"
      ],
      "Resource": "arn:aws:kms:*:*:key/*"
    }
  ]
}
```

**Secrets Manager**:
```
Secrets:
  - ideation/db/password
  - ideation/jwt/secret
  - ideation/api/key
  - ideation/aws/access_key
  - ideation/aws/secret_key
```

### Encryption

**In Transit**:
- TLS 1.2+ for all connections
- HTTPS only (HTTP redirects to HTTPS)
- Encrypted database connections

**At Rest**:
- S3 encryption: AES-256
- RDS encryption: AES-256
- Redis encryption: TLS
- EBS encryption: AES-256

### Backup & Disaster Recovery

**Backup Strategy**:
- Database: Daily automated backups (30-day retention)
- S3: Versioning enabled
- Configuration: Version controlled in Git

**Disaster Recovery**:
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 1 hour
- Multi-AZ deployment for automatic failover
- Cross-region replication (optional)

---

## 11. Deployment Environments

### Development Environment

**Infrastructure**:
```
Docker Compose (single machine):
  - Nginx (1 instance)
  - API (1 instance)
  - PostgreSQL (1 instance)
  - Redis (1 instance)
  - Celery worker (1 instance)
  - Prometheus (1 instance)
  - Grafana (1 instance)
```

**Configuration**:
- Self-signed SSL certificates
- Local storage (no S3)
- In-memory cache (no Redis cluster)
- Single database (no replication)

### Staging Environment

**Infrastructure**:
```
Kubernetes (EKS):
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

**Configuration**:
- AWS Certificate Manager SSL
- S3 for document storage
- Redis cluster with failover
- Multi-AZ database
- Automated backups

### Production Environment

**Infrastructure**:
```
Kubernetes (EKS):
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

**Configuration**:
- AWS Certificate Manager SSL with auto-renewal
- S3 with versioning and lifecycle policies
- Redis cluster with automatic failover
- Multi-AZ database with read replicas
- Automated daily backups with 30-day retention
- Cross-region replication (optional)

---

## 12. Infrastructure as Code (IaC)

### Terraform Configuration

**Directory Structure**:
```
terraform/
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── vpc.tf              # VPC and networking
├── compute.tf          # EC2 and ECS/EKS
├── database.tf         # RDS configuration
├── cache.tf            # ElastiCache configuration
├── storage.tf          # S3 configuration
├── monitoring.tf       # CloudWatch and monitoring
├── security.tf         # IAM and security
└── environments/
    ├── dev.tfvars      # Development variables
    ├── staging.tfvars  # Staging variables
    └── prod.tfvars     # Production variables
```

**Example Terraform Code**:
```hcl
# VPC
resource "aws_vpc" "ideation" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "ideation-vpc"
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "ideation" {
  identifier     = "ideation-db"
  engine         = "postgres"
  engine_version = "12.0"
  instance_class = "db.r5.xlarge"
  allocated_storage = 500
  
  db_name  = "ideation_db"
  username = "ideation_user"
  password = random_password.db_password.result
  
  multi_az            = true
  publicly_accessible = false
  
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  storage_encrypted = true
  kms_key_id       = aws_kms_key.ideation.arn
  
  tags = {
    Name = "ideation-db"
  }
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "ideation" {
  cluster_id           = "ideation-redis"
  engine              = "redis"
  node_type           = "cache.r6g.xlarge"
  num_cache_nodes     = 3
  parameter_group_name = "default.redis6.x"
  engine_version      = "6.0"
  port                = 6379
  
  automatic_failover_enabled = true
  multi_az_enabled          = true
  
  tags = {
    Name = "ideation-redis"
  }
}

# S3 Bucket
resource "aws_s3_bucket" "ideation_documents" {
  bucket = "ideation-documents-prod"

  tags = {
    Name = "ideation-documents"
  }
}

resource "aws_s3_bucket_versioning" "ideation_documents" {
  bucket = aws_s3_bucket.ideation_documents.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ideation_documents" {
  bucket = aws_s3_bucket.ideation_documents.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

---

## 13. Cost Estimation

### Monthly Cost Breakdown (Production)

```
Compute:
  - Nginx (3 instances, t3.medium): $45/month
  - API (5-10 instances, t3.large): $150-300/month
  - Celery Workers (5-10 instances, t3.large): $150-300/month
  - Monitoring (t3.medium): $30/month
  Subtotal: $375-675/month

Database:
  - RDS PostgreSQL (db.r5.xlarge, Multi-AZ): $800/month
  - Backup storage (500 GB): $50/month
  Subtotal: $850/month

Cache:
  - ElastiCache Redis (3 nodes, cache.r6g.xlarge): $600/month
  Subtotal: $600/month

Storage:
  - S3 storage (1 TB): $23/month
  - S3 requests (1M requests): $5/month
  - Data transfer (100 GB): $10/month
  Subtotal: $38/month

Networking:
  - Data transfer (100 GB): $10/month
  - Elastic IPs (2): $7/month
  Subtotal: $17/month

Monitoring:
  - CloudWatch logs (100 GB): $50/month
  - CloudWatch metrics: $10/month
  Subtotal: $60/month

Total Monthly Cost: $1,940-2,240/month
Total Annual Cost: $23,280-26,880/year
```

---

## 14. Scaling Strategy

### Horizontal Scaling

**API Instances**:
- Min: 2 instances
- Max: 10 instances
- Scale up: CPU > 70% for 5 minutes
- Scale down: CPU < 30% for 10 minutes

**Celery Workers**:
- Min: 2 workers
- Max: 10 workers
- Scale up: Queue depth > 100 messages
- Scale down: Queue depth < 10 messages

**Nginx Load Balancer**:
- Min: 2 instances
- Max: 5 instances
- Scale up: CPU > 70% for 5 minutes
- Scale down: CPU < 30% for 10 minutes

### Vertical Scaling

**Database**:
- Monitor CPU and memory usage
- Upgrade instance class if consistently > 80%
- Add read replicas for read-heavy workloads

**Cache**:
- Monitor memory usage
- Upgrade node type if consistently > 85%
- Add more nodes if needed

---

## Summary

**Infrastructure Components**:
- Nginx load balancer (2-5 instances)
- API instances (2-10 instances)
- PostgreSQL RDS (Multi-AZ)
- Redis ElastiCache (3 nodes)
- S3 bucket for documents
- Celery workers (2-10 instances)
- Monitoring stack (Prometheus, Grafana)

**Cloud Platform**: AWS (recommended)

**Networking**: VPC with public/private subnets, security groups

**Security**: IAM roles, encryption, SSL/TLS, Secrets Manager

**Backup & DR**: Daily automated backups, Multi-AZ failover, 4-hour RTO

**Cost**: $1,940-2,240/month ($23,280-26,880/year)

**Scalability**: Horizontal scaling for compute, vertical scaling for database

