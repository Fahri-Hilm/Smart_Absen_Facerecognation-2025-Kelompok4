#!/bin/bash

echo "🚀 Starting Smart Absen MySQL Server..."

# Create directory if not exists
mkdir -p mysql-server

# Start MySQL server
cd mysql-server
docker compose up -d

echo "⏳ Waiting for MySQL to be ready..."
sleep 15

# Test connection
echo "🔍 Testing MySQL connection..."
docker exec smart_absen_mysql mysql -u absen_user -pAbsenPass2025! -e "SHOW DATABASES;"

echo "✅ MySQL Server is ready!"
echo ""
echo "📋 Database Connection Info:"
echo "Host: localhost (or your-server-ip)"
echo "Port: 3306"
echo "Database: smart_absen"
echo "Username: absen_user"
echo "Password: AbsenPass2025!"
echo "Root Password: SmartAbsen2025!"
echo ""
echo "🔗 Connection String:"
echo "mysql://absen_user:AbsenPass2025!@localhost:3306/smart_absen"
