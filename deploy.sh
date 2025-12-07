#!/bin/bash

# Smart Absen Docker Deployment Script
# Usage: ./deploy.sh [version]

set -e

VERSION=${1:-"2.0"}
IMAGE_NAME="smart-absen"
REGISTRY="ghcr.io"
USERNAME="fahri-hilm"
REPO="smart_absen_facerecognation-2025-kelompok4"

echo "🐳 Building Docker image..."
docker build -t ${IMAGE_NAME}:${VERSION} .

echo "🏷️  Tagging images..."
docker tag ${IMAGE_NAME}:${VERSION} ${REGISTRY}/${USERNAME}/${REPO}:${VERSION}
docker tag ${IMAGE_NAME}:${VERSION} ${REGISTRY}/${USERNAME}/${REPO}:latest

echo "📤 Pushing to GitHub Container Registry..."
docker push ${REGISTRY}/${USERNAME}/${REPO}:${VERSION}
docker push ${REGISTRY}/${USERNAME}/${REPO}:latest

echo "✅ Deployment complete!"
echo ""
echo "Pull with:"
echo "  docker pull ${REGISTRY}/${USERNAME}/${REPO}:${VERSION}"
echo "  docker pull ${REGISTRY}/${USERNAME}/${REPO}:latest"
