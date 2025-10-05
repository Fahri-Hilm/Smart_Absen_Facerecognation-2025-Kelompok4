#!/usr/bin/env python3
"""
Debug script untuk memeriksa masalah GUI kamera pada absen pulang
"""

import cv2
import os
import sys
from datetime import datetime

def test_camera_gui(mode='test'):
    """Test camera GUI dengan mode tertentu"""
    print(f"[DEBUG] Testing camera GUI for mode: {mode}")
    
    # Test kamera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open camera!")
        return False
        
    print("[INFO] Camera opened successfully")
    
    frame_count = 0
    start_time = datetime.now()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Cannot read frame from camera")
                break
                
            frame_count += 1
            
            # Add text overlay
            cv2.putText(frame, f'Mode: {mode.upper()}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Frame: {frame_count}', (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, 'Press ESC to exit', (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Show frame
            window_name = f"Debug Camera - {mode}"
            cv2.imshow(window_name, frame)
            print(f"[DEBUG] Frame {frame_count} displayed")
            
            # Check for ESC key
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("[INFO] ESC pressed, exiting...")
                break
                
            # Auto exit after 10 seconds for testing
            if (datetime.now() - start_time).seconds > 10:
                print("[INFO] Auto exit after 10 seconds")
                break
                
    except Exception as e:
        print(f"[ERROR] Exception in camera loop: {e}")
        
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"[INFO] Camera released, total frames: {frame_count}")
        
    return True

def check_opencv_environment():
    """Check OpenCV environment and GUI backend"""
    print(f"[INFO] OpenCV version: {cv2.__version__}")
    
    # Check backends
    backends = []
    for backend in ['QT', 'GTK', 'X11']:
        try:
            if hasattr(cv2, f'WINDOW_{backend}'):
                backends.append(backend)
        except:
            pass
    
    print(f"[INFO] Available GUI backends: {backends}")
    
    # Check display
    display = os.environ.get('DISPLAY', 'Not set')
    print(f"[INFO] DISPLAY environment: {display}")
    
    # Check if running in SSH or headless
    ssh_connection = os.environ.get('SSH_CONNECTION', None)
    if ssh_connection:
        print(f"[WARNING] SSH connection detected: {ssh_connection}")
    
    return True

if __name__ == "__main__":
    print("=== Camera GUI Debug Script ===")
    
    # Check environment
    check_opencv_environment()
    
    print("\n=== Testing Camera GUI ===")
    
    # Test different modes
    modes = ['masuk', 'pulang', 'test']
    
    for mode in modes:
        print(f"\n--- Testing mode: {mode} ---")
        success = test_camera_gui(mode)
        if not success:
            print(f"[ERROR] Failed to test mode: {mode}")
            break
        
        # Wait a bit between tests
        import time
        time.sleep(2)
    
    print("\n=== Debug Complete ===")