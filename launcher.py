#!/usr/bin/env python3
"""
Kafebasabasi Attendance System Launcher
Launcher untuk menjalankan sistem dalam berbagai mode
"""

import os
import sys
import subprocess

def print_banner():
    print("🚀 KAFEBASABASI ATTENDANCE SYSTEM - LAUNCHER")
    print("=" * 50)
    print()

def show_menu():
    print("Pilih mode yang ingin dijalankan:")
    print()
    print("1. 🔄 DUAL MODE (Local + Ngrok) - Recommended")
    print("2. 🏠 LOCAL ONLY (Tanpa Ngrok)")
    print("3. 🌐 NGROK FORCED (Paksa Ngrok)")
    print("4. 🎥 CAMERA TEST (Test Kamera Saja)")
    print("5. ❌ EXIT")
    print()

def run_dual_mode():
    print("🔄 Starting DUAL MODE (Local + Ngrok)...")
    print("📍 Local access: http://localhost:5001")
    print("🌐 Public access: akan ditampilkan jika ngrok berhasil")
    print("💡 Mode ini otomatis fallback ke local jika ngrok gagal")
    print()
    
    # Set environment untuk dual mode (default)
    env = os.environ.copy()
    env['USE_NGROK'] = 'true'
    return subprocess.run([sys.executable, 'app.py'], env=env)

def run_local_only():
    print("🏠 Starting LOCAL ONLY mode...")
    print("📍 Hanya akses local: http://localhost:5001")
    print("💡 Ngrok dinonaktifkan sepenuhnya")
    print()
    
    env = os.environ.copy()
    env['LOCAL_ONLY'] = 'true'
    return subprocess.run([sys.executable, 'app.py'], env=env)

def run_ngrok_forced():
    print("🌐 Starting dengan NGROK FORCED...")
    print("📍 Local access: http://localhost:5001")
    print("🌐 Public access: dipaksa aktif")
    print("⚠️ Akan error jika ngrok tidak terinstall")
    print()
    
    env = os.environ.copy()
    env['USE_NGROK'] = 'true'
    env['LOCAL_ONLY'] = 'false'
    return subprocess.run([sys.executable, 'app.py'], env=env)

def run_camera_test():
    print("🎥 Starting CAMERA TEST mode...")
    print("📍 Test kamera: http://localhost:5002/camera-test")
    print("💡 Mode khusus untuk testing kamera saja")
    print()
    
    # Run simple camera test server
    camera_test_code = '''
import os
import sys
from flask import Flask, render_template, jsonify
import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'test_secret_key'

@app.route('/camera-test')
def camera_test():
    return render_template('camera_test.html')

@app.route('/test-api/cameras')
def test_api_cameras():
    try:
        cameras = []
        
        # Test camera 0
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    
                    cameras.append({
                        'id': 0,
                        'name': 'Webcam Default',
                        'status': 'active',
                        'resolution': f'{width}x{height}',
                        'fps': fps
                    })
                    logger.info(f'Camera 0 detected: {width}x{height} @ {fps}fps')
                cap.release()
        except Exception as e:
            logger.error(f'Camera 0 error: {e}')
        
        return jsonify({
            'cameras': cameras,
            'total_detected': len(cameras),
            'active_count': len([cam for cam in cameras if cam['status'] == 'active'])
        })
        
    except Exception as e:
        logger.error(f'API Error: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('🎥 Simple Camera Test Server')
    print('Camera Test: http://localhost:5002/camera-test')
    print('API Test: http://localhost:5002/test-api/cameras')
    app.run(host='127.0.0.1', port=5002, debug=False)
'''
    
    return subprocess.run([sys.executable, '-c', camera_test_code])

def main():
    print_banner()
    
    while True:
        show_menu()
        
        try:
            choice = input("Masukkan pilihan (1-5): ").strip()
            
            if choice == '1':
                result = run_dual_mode()
                return result.returncode if result else 0
            elif choice == '2':
                result = run_local_only()
                return result.returncode if result else 0
            elif choice == '3':
                result = run_ngrok_forced()
                return result.returncode if result else 0
            elif choice == '4':
                result = run_camera_test()
                return result.returncode if result else 0
            elif choice == '5':
                print("👋 Goodbye!")
                return 0
            else:
                print("❌ Pilihan tidak valid! Silakan pilih 1-5.")
                print()
                continue
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return 0
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

if __name__ == '__main__':
    sys.exit(main())