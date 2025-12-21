#!/bin/bash

echo "🔧 Smart Absen - Camera Fix Script"
echo "=================================="

# Check if camera device exists
echo "1. Checking camera hardware..."
if ls /dev/video* 1> /dev/null 2>&1; then
    echo "✅ Camera device found: $(ls /dev/video*)"
else
    echo "❌ No camera device found!"
    echo "   Please check camera connection"
    exit 1
fi

# Check camera permissions
echo "2. Checking camera permissions..."
if [ -r /dev/video0 ]; then
    echo "✅ Camera permissions OK"
else
    echo "⚠️  Camera permission issue, trying to fix..."
    sudo chmod 666 /dev/video0
fi

# Check if camera is in use
echo "3. Checking if camera is in use..."
if sudo lsof /dev/video0 2>/dev/null; then
    echo "⚠️  Camera is in use by another process"
    echo "   Please close other camera applications"
else
    echo "✅ Camera is available"
fi

# Test camera with v4l2
echo "4. Testing camera with v4l2..."
if command -v v4l2-ctl &> /dev/null; then
    v4l2-ctl --list-devices
    echo "✅ Camera test completed"
else
    echo "⚠️  v4l2-utils not installed, installing..."
    sudo apt update && sudo apt install -y v4l-utils
fi

# Check Flask app
echo "5. Checking Flask application..."
if pgrep -f "python3 app.py" > /dev/null; then
    echo "✅ Flask app is running"
    echo "   Camera debug: http://localhost:5001/camera-debug"
    echo "   Add employee: http://localhost:5001/admin/add_employee_form"
else
    echo "❌ Flask app not running, starting..."
    cd "$(dirname "$0")"
    nohup python3 app.py > app_output.log 2>&1 &
    sleep 3
    if pgrep -f "python3 app.py" > /dev/null; then
        echo "✅ Flask app started successfully"
    else
        echo "❌ Failed to start Flask app"
        echo "   Check app_output.log for errors"
    fi
fi

echo ""
echo "🚀 Next Steps:"
echo "1. Open browser: http://localhost:5001/camera-debug"
echo "2. Allow camera permission when prompted"
echo "3. If camera works, go to: http://localhost:5001/admin/add_employee_form"
echo "4. If still not working, check CAMERA_TROUBLESHOOTING.md"
echo ""
echo "✅ Camera fix script completed!"
