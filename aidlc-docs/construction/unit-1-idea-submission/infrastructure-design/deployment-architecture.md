# Unit 1: Idea Submission & Management - Deployment Architecture

## Overview
This document defines the deployment architecture for Unit 1, including containerization, orchestration, CI/CD pipeline, and deployment procedures.

---

## 1. Containerization Strategy

### Docker Images

**API Image**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "30", "app.wsgi"]
```

**Celery Worker Image**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    clamav \
    clamav-daemon \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run Celery worker
CMD ["celery", "-A", "app.celery", "worker", "--loglevel=info", "--concurrency=4"]
```

**Nginx Image**:
```dockerfile
FROM nginx:1.21-alpine

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Copy SSL certificates
COPY certs/ /etc/nginx/certs/

# Create non-root user
RUN addgroup -g 1000 nginx && adduser -u 1000 -G nginx -s /sbin/nologin nginx

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose (Development)

```yaml
version: '3.8'

services:
  nginx:
    build:
      context: .
      dockerfile: Dockerfile.nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - api
    networks:
      - ideation

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://ideation_user:password@postgres:5432/ideation_db
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=True
    volumes:
      - .:/app
    depends_on:
      - postgres
      - redis
    networks:
      - ideation

  postgres:
    image: postgres:12-alpine
    environment:
      - POSTGRES_DB=ideation_db
      - POSTGRES_USER=ideation_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - ideation

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - ideation

  celery:
    build:
      context: .
      dockerfile: Dockerfile.celery
    environment:
      - DATABASE_URL=postgresql://ideation_user:password@postgres:5432/ideation_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - .:/app
    depends_on:
      - postgres
      - redis
    networks:
      - ideation

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - ideation

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - ideation

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  ideation:
    driver: bridge
```

---

## 2. Kubernetes Deployment

### Kubernetes Manifests

**Namespace**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ideation
```

**ConfigMap (Environment Variables)**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ideation-config
  namespace: ideation
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  ALLOWED_HOSTS: "ideation.example.com,api.ideation.example.com"
```

**Secret (Credentials)**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ideation-secrets
  namespace: ideation
type: Opaque
stringData:
  DATABASE_URL: "postgresql://ideation_user:password@postgres.ideation.svc.cluster.local:5432/ideation_db"
  REDIS_URL: "redis://redis.ideation.svc.cluster.local:6379/0"
  JWT_SECRET: "your-secret-key-here"
  AWS_ACCESS_KEY_ID: "your-access-key"
  AWS_SECRET_ACCESS_KEY: "your-secret-key"
```

**API Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ideation-api
  namespace: ideation
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
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
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        
        envFrom:
        - configMapRef:
            name: ideation-config
        - secretRef:
            name: ideation-secrets
        
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
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        volumeMounts:
        - name: logs
          mountPath: /app/logs
      
      volumes:
      - name: logs
        emptyDir: {}
      
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - ideation-api
              topologyKey: kubernetes.io/hostname
```

**API Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ideation-api
  namespace: ideation
spec:
  type: ClusterIP
  selector:
    app: ideation-api
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
    name: http
```

**Celery Worker Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ideation-celery
  namespace: ideation
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ideation-celery
  template:
    metadata:
      labels:
        app: ideation-celery
    spec:
      containers:
      - name: celery
        image: ideation-celery:latest
        imagePullPolicy: Always
        
        envFrom:
        - configMapRef:
            name: ideation-config
        - secretRef:
            name: ideation-secrets
        
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi
```

**Nginx Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ideation-nginx
  namespace: ideation
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ideation-nginx
  template:
    metadata:
      labels:
        app: ideation-nginx
    spec:
      containers:
      - name: nginx
        image: ideation-nginx:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 80
          name: http
        - containerPort: 443
          name: https
        
        resources:
          requests:
            cpu: 250m
            memory: 512Mi
          limits:
            cpu: 500m
            memory: 1Gi
        
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/conf.d
          readOnly: true
        - name: ssl-certs
          mountPath: /etc/nginx/certs
          readOnly: true
      
      volumes:
      - name: nginx-config
        configMap:
          name: nginx-config
      - name: ssl-certs
        secret:
          secretName: ssl-certs
```

**Nginx Service (LoadBalancer)**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ideation-nginx
  namespace: ideation
spec:
  type: LoadBalancer
  selector:
    app: ideation-nginx
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  - port: 443
    targetPort: 443
    protocol: TCP
    name: https
```

**Horizontal Pod Autoscaler**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ideation-api-hpa
  namespace: ideation
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ideation-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 3. CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: Build and Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:12
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:6
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        files: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    
    - name: Log in to Container Registry
      uses: docker/login-action@v1
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v3
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha
    
    - name: Build and push API image
      uses: docker/build-push-action@v2
      with:
        context: .
        file: ./Dockerfile.api
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
    
    - name: Build and push Celery image
      uses: docker/build-push-action@v2
      with:
        context: .
        file: ./Dockerfile.celery
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}-celery
        labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    steps:
    - uses: actions/checkout@v2
    
    - name: Configure kubectl
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
        chmod 600 $HOME/.kube/config
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/ideation-api \
          api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n ideation
        kubectl set image deployment/ideation-celery \
          celery=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}-celery \
          -n ideation
        kubectl rollout status deployment/ideation-api -n ideation
        kubectl rollout status deployment/ideation-celery -n ideation
```

---

## 4. Deployment Procedures

### Pre-Deployment Checklist

```
[ ] Code review completed
[ ] All tests passing
[ ] Security scan completed
[ ] Database migrations tested
[ ] Configuration updated
[ ] Secrets configured
[ ] Backup created
[ ] Rollback plan documented
[ ] Monitoring alerts configured
[ ] Team notified
```

### Deployment Steps

**1. Staging Deployment**:
```bash
# Build images
docker build -f Dockerfile.api -t ideation-api:staging .
docker build -f Dockerfile.celery -t ideation-celery:staging .

# Push to registry
docker push ideation-api:staging
docker push ideation-celery:staging

# Deploy to staging
kubectl set image deployment/ideation-api \
  api=ideation-api:staging -n ideation-staging
kubectl set image deployment/ideation-celery \
  celery=ideation-celery:staging -n ideation-staging

# Wait for rollout
kubectl rollout status deployment/ideation-api -n ideation-staging
kubectl rollout status deployment/ideation-celery -n ideation-staging

# Run smoke tests
pytest tests/smoke/ --env=staging
```

**2. Production Deployment**:
```bash
# Tag images
docker tag ideation-api:staging ideation-api:v1.0.0
docker tag ideation-celery:staging ideation-celery:v1.0.0

# Push to registry
docker push ideation-api:v1.0.0
docker push ideation-celery:v1.0.0

# Deploy to production
kubectl set image deployment/ideation-api \
  api=ideation-api:v1.0.0 -n ideation
kubectl set image deployment/ideation-celery \
  celery=ideation-celery:v1.0.0 -n ideation

# Monitor rollout
kubectl rollout status deployment/ideation-api -n ideation
kubectl rollout status deployment/ideation-celery -n ideation

# Verify deployment
curl https://ideation.example.com/health
```

### Rollback Procedure

```bash
# If deployment fails, rollback immediately
kubectl rollout undo deployment/ideation-api -n ideation
kubectl rollout undo deployment/ideation-celery -n ideation

# Verify rollback
kubectl rollout status deployment/ideation-api -n ideation
kubectl rollout status deployment/ideation-celery -n ideation

# Check logs
kubectl logs -f deployment/ideation-api -n ideation
```

---

## 5. Database Migrations

### Migration Strategy

**Development**:
```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

**Staging/Production**:
```bash
# Create migration
python manage.py makemigrations

# Test migration
python manage.py migrate --plan

# Apply migration (with backup)
# 1. Create backup
aws rds create-db-snapshot --db-instance-identifier ideation-db --db-snapshot-identifier ideation-db-backup-$(date +%s)

# 2. Apply migration
python manage.py migrate

# 3. Verify migration
python manage.py check
```

### Zero-Downtime Migrations

**Strategy**:
1. Deploy code that supports both old and new schema
2. Run migration
3. Deploy code that uses new schema
4. Remove old schema support

**Example**:
```python
# Step 1: Add new field (backward compatible)
class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    new_field = models.CharField(max_length=100, null=True, blank=True)

# Step 2: Migrate data
python manage.py migrate

# Step 3: Deploy code using new field
# Step 4: Remove old field in next migration
```

---

## 6. Monitoring & Alerting

### Prometheus Scrape Configuration

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ideation-api'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - ideation
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: ideation-api
      - source_labels: [__meta_kubernetes_pod_container_port_number]
        action: keep
        regex: "8000"

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Alert Rules

```yaml
groups:
  - name: ideation_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}"
      
      - alert: SlowAPIResponse
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 5m
        annotations:
          summary: "API response time is slow"
          description: "p95 response time is {{ $value }}s"
      
      - alert: DatabaseConnectionPoolExhausted
        expr: db_active_connections > 80
        for: 2m
        annotations:
          summary: "Database connection pool exhausted"
          description: "Active connections: {{ $value }}"
```

---

## 7. Backup & Disaster Recovery

### Backup Strategy

**Database Backups**:
```bash
# Automated daily backups (AWS RDS)
# Retention: 30 days
# Backup window: 03:00-04:00 UTC

# Manual backup before major changes
aws rds create-db-snapshot \
  --db-instance-identifier ideation-db \
  --db-snapshot-identifier ideation-db-backup-$(date +%Y%m%d-%H%M%S)
```

**S3 Backups**:
```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ideation-documents-prod \
  --versioning-configuration Status=Enabled

# Enable cross-region replication
aws s3api put-bucket-replication \
  --bucket ideation-documents-prod \
  --replication-configuration file://replication.json
```

### Disaster Recovery

**RTO (Recovery Time Objective)**: 4 hours
**RPO (Recovery Point Objective)**: 1 hour

**Recovery Procedure**:
```bash
# 1. Restore database from backup
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier ideation-db-restored \
  --db-snapshot-identifier ideation-db-backup-20231228-120000

# 2. Update DNS to point to restored database
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch file://dns-update.json

# 3. Restore S3 bucket from backup
aws s3 sync s3://ideation-documents-backup s3://ideation-documents-prod

# 4. Verify application
curl https://ideation.example.com/health

# 5. Notify stakeholders
```

---

## Summary

**Containerization**: Docker images for API, Celery, and Nginx

**Orchestration**: Kubernetes (EKS) with auto-scaling

**CI/CD**: GitHub Actions with automated testing and deployment

**Deployment**: Rolling updates with zero downtime

**Monitoring**: Prometheus, Grafana, CloudWatch

**Backup & DR**: Daily automated backups, 4-hour RTO, 1-hour RPO

**Cost**: $1,940-2,240/month for production infrastructure

