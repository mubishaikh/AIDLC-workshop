#!/bin/bash

# Ideation Portal - Build Script
# This script builds Docker images for the Ideation Portal

set -e

echo "=========================================="
echo "Ideation Portal - Docker Build Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="${REGISTRY:-ideation}"
BACKEND_IMAGE="${REGISTRY}/ideation-api:latest"
FRONTEND_IMAGE="${REGISTRY}/ideation-frontend:latest"

# Functions
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[i]${NC} $1"
}

# Check prerequisites
print_info "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed"
    exit 1
fi

print_status "Docker and Docker Compose are installed"

# Build backend image
print_info "Building backend image: $BACKEND_IMAGE"
docker build -t "$BACKEND_IMAGE" ./backend
print_status "Backend image built successfully"

# Build frontend image
print_info "Building frontend image: $FRONTEND_IMAGE"
docker build -t "$FRONTEND_IMAGE" ./frontend
print_status "Frontend image built successfully"

# List images
print_info "Built images:"
docker images | grep ideation

# Summary
echo ""
echo "=========================================="
echo "Build Complete!"
echo "=========================================="
echo ""
echo "Backend image:  $BACKEND_IMAGE"
echo "Frontend image: $FRONTEND_IMAGE"
echo ""
echo "Next steps:"
echo "1. Push images to registry:"
echo "   docker push $BACKEND_IMAGE"
echo "   docker push $FRONTEND_IMAGE"
echo ""
echo "2. Deploy to staging:"
echo "   kubectl apply -f k8s/deployment.yaml -n ideation-staging"
echo ""
echo "3. Or run locally with Docker Compose:"
echo "   docker-compose up -d"
echo ""
