# Ideation Portal - Deployment Guide

## Immediate Actions Checklist

### 1. Build Docker Images ✅
```bash
# Build backend image
docker build -t ideation-api:latest ./backend

# Build frontend image
docker build -t ideation-frontend:latest ./frontend

# Verify images
docker images | grep ideation
```

### 2. Push to Container Registry
```bash
# Login to registry (AWS ECR example)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag images
docker tag ideation-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ideation-api:latest
docker tag ideation-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ideation-frontend:latest

# Push images
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ideation-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ideation-frontend:latest
```

### 3. Deploy to Staging Environment
```bash
# Create namespace
kubectl create namespace ideation-staging

# Create secrets
kubectl create secret generic ideation-secrets \
  --from-literal=secret-key='your-secret-key' \
  --from-literal=database-url='postgresql://user:pass@host:5432/db' \
  --from-literal=redis-url='redis://host:6379/0' \
  -n ideation-staging

# Deploy application
kubectl apply -f k8s/deployment.yaml -n ideation-staging

# Verify deployment
kubectl get deployments -n ideation-staging
kubectl get pods -n ideation-staging
kubectl get services -n ideation-staging
```

### 4. Run Integration Tests
```bash
# Run backend tests
cd backend
pytest --cov=. --cov-report=html

# Run frontend tests
cd ../frontend
npm test -- --coverage

# View coverage reports
# Backend: backend/htmlcov/index.html
# Frontend: frontend/coverage/index.html
```

### 5. Performance Testing
```bash
# Install load testing tool
pip install locust

# Run load test
locust -f locustfile.py --host=http://staging-api.example.com

# Monitor metrics
# Prometheus: http://staging-prometheus.example.com:9090
# Grafana: http://staging-grafana.example.com:3000
```

### 6. Security Testing
```bash
# Run security scan
docker run --rm -v $(pwd):/src aquasec/trivy image ideation-api:latest

# Run OWASP ZAP scan
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://staging-api.example.com
```

---

## Development Environment Setup

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.9+
- Node.js 18+
- PostgreSQL 12+ (optional, Docker handles it)
- Redis 6+ (optional, Docker handles it)

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd ideation-portal

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access services
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/v1
# Admin: http://localhost:8000/admin
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
```

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Staging Environment Setup

### Prerequisites
- AWS Account with EKS cluster
- kubectl configured
- AWS CLI configured
- Container registry (ECR)

### Deployment Steps
```bash
# 1. Create namespace
kubectl create namespace ideation-staging

# 2. Create secrets
kubectl create secret generic ideation-secrets \
  --from-literal=secret-key='<generate-secure-key>' \
  --from-literal=database-url='postgresql://user:pass@rds-endpoint:5432/ideation_db' \
  --from-literal=redis-url='redis://elasticache-endpoint:6379/0' \
  -n ideation-staging

# 3. Update image references in deployment.yaml
# Replace <account-id> with your AWS account ID

# 4. Deploy
kubectl apply -f k8s/deployment.yaml -n ideation-staging

# 5. Verify deployment
kubectl get all -n ideation-staging

# 6. Get service endpoint
kubectl get service ideation-api -n ideation-staging
```

### Monitoring
```bash
# View logs
kubectl logs -f deployment/ideation-api -n ideation-staging

# Port forward to local machine
kubectl port-forward svc/ideation-api 8000:8000 -n ideation-staging

# Access Prometheus
kubectl port-forward svc/prometheus 9090:9090 -n ideation-staging

# Access Grafana
kubectl port-forward svc/grafana 3000:3000 -n ideation-staging
```

---

## Production Environment Setup

### Prerequisites
- AWS Account with production EKS cluster
- Multi-AZ RDS PostgreSQL
- ElastiCache Redis cluster
- S3 bucket for documents
- CloudFront distribution
- Route 53 DNS
- AWS Certificate Manager SSL certificate

### Deployment Steps
```bash
# 1. Create namespace
kubectl create namespace ideation

# 2. Create secrets
kubectl create secret generic ideation-secrets \
  --from-literal=secret-key='<generate-secure-key>' \
  --from-literal=database-url='postgresql://user:pass@prod-rds-endpoint:5432/ideation_db' \
  --from-literal=redis-url='redis://prod-elasticache-endpoint:6379/0' \
  -n ideation

# 3. Update image references
# Replace with production image registry

# 4. Deploy
kubectl apply -f k8s/deployment.yaml -n ideation

# 5. Verify deployment
kubectl get all -n ideation

# 6. Configure ingress (optional)
# Create ingress for external access
```

### Monitoring & Alerting
```bash
# Configure Prometheus alerts
kubectl apply -f k8s/prometheus-rules.yaml -n ideation

# Configure Grafana dashboards
# Import dashboards from k8s/grafana-dashboards/

# Set up PagerDuty/Slack integration
# Configure AlertManager for notifications
```

---

## Troubleshooting

### Common Issues

**1. Pod not starting**
```bash
# Check pod status
kubectl describe pod <pod-name> -n ideation-staging

# Check logs
kubectl logs <pod-name> -n ideation-staging

# Check events
kubectl get events -n ideation-staging
```

**2. Database connection error**
```bash
# Verify database URL
kubectl get secret ideation-secrets -o jsonpath='{.data.database-url}' -n ideation-staging | base64 -d

# Test connection
kubectl run -it --rm debug --image=postgres:12 --restart=Never -- psql <database-url>
```

**3. Redis connection error**
```bash
# Verify Redis URL
kubectl get secret ideation-secrets -o jsonpath='{.data.redis-url}' -n ideation-staging | base64 -d

# Test connection
kubectl run -it --rm debug --image=redis:6 --restart=Never -- redis-cli -u <redis-url> ping
```

**4. API not responding**
```bash
# Check service
kubectl get service ideation-api -n ideation-staging

# Check endpoints
kubectl get endpoints ideation-api -n ideation-staging

# Port forward and test
kubectl port-forward svc/ideation-api 8000:8000 -n ideation-staging
curl http://localhost:8000/api/v1/health
```

---

## Rollback Procedure

### Kubernetes Rollback
```bash
# View rollout history
kubectl rollout history deployment/ideation-api -n ideation-staging

# Rollback to previous version
kubectl rollout undo deployment/ideation-api -n ideation-staging

# Rollback to specific revision
kubectl rollout undo deployment/ideation-api --to-revision=2 -n ideation-staging

# Verify rollback
kubectl rollout status deployment/ideation-api -n ideation-staging
```

---

## Monitoring Dashboard

### Prometheus Queries
```
# API request rate
rate(http_requests_total[5m])

# API error rate
rate(http_requests_total{status=~"5.."}[5m])

# API response time (p95)
histogram_quantile(0.95, http_request_duration_seconds)

# Database connections
db_active_connections

# Redis memory usage
redis_used_memory_bytes
```

### Grafana Dashboards
- System Health (CPU, memory, disk)
- API Performance (requests, latency, errors)
- Database Performance (queries, connections)
- Business Metrics (ideas, submissions)

---

## Support & Documentation

- **API Documentation**: http://api.example.com/docs
- **Architecture Guide**: See `aidlc-docs/construction/unit-1-idea-submission/infrastructure-design/`
- **Deployment Guide**: This file
- **Troubleshooting**: See section above

---

## Contact

For deployment issues or questions, contact the DevOps team.

