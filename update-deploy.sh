#!/bin/bash

# Update deployment script untuk VPS
# Usage: ./update-deploy.sh

set -e

echo "🔄 Updating Smart Absen from GitHub..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Pull latest changes from GitHub
echo "📥 Pulling latest changes..."
git pull origin main

# Rebuild images with latest changes
echo "🔨 Rebuilding Docker images..."
docker-compose build --no-cache

# Start services
echo "🚀 Starting updated services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Check if database needs initialization
echo "🗄️ Checking database..."
docker-compose exec -T app python -c "
from database import db_manager
try:
    db_manager.initialize_database()
    print('Database initialized successfully')
except Exception as e:
    print(f'Database already exists or error: {e}')
"

echo "✅ Update completed!"
echo ""
echo "🌐 Application updated at: http://your-vps-ip:5001"
echo ""
echo "📋 Check status:"
echo "  - View logs: docker-compose logs -f"
echo "  - Check containers: docker-compose ps"
