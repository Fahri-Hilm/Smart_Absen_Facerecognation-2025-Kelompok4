#!/bin/bash

# Docker Deployment Script untuk Smart Absen Face Recognition
# Usage: ./deploy.sh

set -e

echo "🚀 Starting Smart Absen deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker tidak terinstall. Install Docker terlebih dahulu."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose tidak terinstall. Install Docker Compose terlebih dahulu."
    exit 1
fi

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs face_data Attendance

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build --no-cache

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Initialize database
echo "🗄️ Initializing database..."
docker-compose exec app python database.py

echo "✅ Deployment completed!"
echo ""
echo "🌐 Application is running at: http://localhost:5001"
echo "🗄️ MySQL is running at: localhost:3306"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart: docker-compose restart"
echo "  - Update: git pull && docker-compose build --no-cache && docker-compose up -d"
