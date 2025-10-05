#!/bin/bash
echo "🏠 Starting Kafebasabasi - LOCAL ONLY MODE"
echo "============================================="
echo "📍 Hanya bisa diakses dari komputer lokal"
echo "🔗 URL: http://localhost:5001"
echo "============================================="

export USE_NGROK=false
cd "$(dirname "$0")/.." && /usr/bin/python3 app.py