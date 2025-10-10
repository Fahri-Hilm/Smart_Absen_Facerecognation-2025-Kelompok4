#!/usr/bin/env python3
"""
Test script untuk menjalankan server Flask tanpa ngrok
Fokus pada testing kamera lokal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import cv2
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'test_secret_key_for_camera_testing'

# Simple admin auth
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect('/admin/camera')
        else:
            return render_template('admin_login.html', error='Login gagal')
    
    return render_template('admin_login.html')

@app.route('/admin/camera')
def admin_camera():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')
    return render_template('admin_camera.html')

@app.route('/admin/api/cameras')
def admin_get_cameras():
    """API untuk admin mendapatkan daftar kamera yang tersedia"""
    try:
        import os
        
        # Deteksi kamera yang tersedia
        cameras = []
        
        # Test kamera 0 (default webcam)
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    # Get resolution info
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    
                    cameras.append({
                        'id': 0,
                        'name': 'Webcam Default',
                        'status': 'active',
                        'device': '/dev/video0',
                        'resolution': f'{width}x{height}',
                        'fps': fps
                    })
                    logger.info(f"Camera 0 detected: {width}x{height} @ {fps}fps")
                else:
                    cameras.append({
                        'id': 0,
                        'name': 'Webcam Default',
                        'status': 'detected_but_no_signal',
                        'device': '/dev/video0'
                    })
                cap.release()
            else:
                cameras.append({
                    'id': 0,
                    'name': 'Webcam Default',
                    'status': 'not_accessible',
                    'device': '/dev/video0'
                })
        except Exception as e:
            logger.error(f"Error testing camera 0: {e}")
            cameras.append({
                'id': 0,
                'name': 'Webcam Default',
                'status': 'error',
                'device': '/dev/video0',
                'error': str(e)
            })
        
        # Test kamera 1 jika ada
        try:
            cap = cv2.VideoCapture(1)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    
                    cameras.append({
                        'id': 1,
                        'name': 'Webcam Eksternal',
                        'status': 'active',
                        'device': '/dev/video1',
                        'resolution': f'{width}x{height}',
                        'fps': fps
                    })
                    logger.info(f"Camera 1 detected: {width}x{height} @ {fps}fps")
                cap.release()
        except Exception as e:
            logger.warning(f"Camera 1 not available: {e}")
        
        # Jika tidak ada kamera yang bekerja, beri pesan yang jelas
        active_cameras = [cam for cam in cameras if cam['status'] == 'active']
        if not active_cameras:
            logger.warning("No active cameras detected!")
        
        return jsonify({
            'cameras': cameras,
            'total_detected': len(cameras),
            'active_count': len(active_cameras),
            'message': f"Found {len(active_cameras)} working camera(s)" if active_cameras else "No working cameras found. Please check camera connection."
        })
        
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        return jsonify({
            'cameras': [{
                'id': 0,
                'name': 'Error - Camera Detection Failed',
                'status': 'system_error',
                'device': 'unknown',
                'error': str(e)
            }],
            'total_detected': 0,
            'active_count': 0,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🎥 Camera Test Server Starting...")
    print("🌐 Local URL: http://localhost:5001")
    print("👨‍💼 Admin Login: http://localhost:5001/admin/login")
    print("📷 Camera Config: http://localhost:5001/admin/camera")
    print("💡 Login: admin / admin")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True)