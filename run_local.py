#!/usr/bin/env python3
"""
Script untuk menjalankan aplikasi absensi tanpa ngrok (local only)
Fokus pada testing kamera
"""

import os
import sys

# Disable ngrok by setting environment variable
os.environ['NO_NGROK'] = '1'

# Import dan jalankan aplikasi asli
if __name__ == '__main__':
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # Import app
    from app import app, logger
    
    print("🎥 KAFEBASABASI ATTENDANCE (Camera Test Mode)")
    print("=" * 50)
    print("🌐 Local URL: http://localhost:5001")
    print("👨‍💼 Admin Login: http://localhost:5001/admin/login")
    print("📷 Camera Config: http://localhost:5001/admin/camera")
    print("💡 Username: admin, Password: admin123")
    print("=" * 50)
    
    # Run app in local mode only
    app.run(host='127.0.0.1', port=5001, debug=False)