#!/usr/bin/env python3
"""
Script sederhana untuk test kamera OpenCV
"""

import cv2
import sys

def test_camera(camera_index):
    """Test kamera dengan index tertentu"""
    print(f"Testing camera {camera_index}...")
    
    try:
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"❌ Camera {camera_index}: Cannot open")
            return False
            
        # Read frame
        ret, frame = cap.read()
        
        if ret and frame is not None:
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            print(f"✅ Camera {camera_index}: Active")
            print(f"   Resolution: {width}x{height}")
            print(f"   FPS: {fps}")
            print(f"   Frame shape: {frame.shape}")
            
            cap.release()
            return True
        else:
            print(f"⚠️ Camera {camera_index}: Opened but no frame")
            cap.release()
            return False
            
    except Exception as e:
        print(f"❌ Camera {camera_index}: Error - {e}")
        return False

def main():
    """Main function"""
    print("🎥 Camera Detection Test")
    print("=" * 30)
    
    # Test cameras 0-2
    active_cameras = []
    
    for i in range(3):
        if test_camera(i):
            active_cameras.append(i)
        print()
    
    print("Summary:")
    print(f"Active cameras: {active_cameras}")
    
    if active_cameras:
        print(f"\n✅ Found {len(active_cameras)} working camera(s)")
        
        # Test with a simple preview for first camera
        camera_id = active_cameras[0]
        print(f"\nTesting preview for camera {camera_id}...")
        
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Frame capture successful!")
                print(f"Frame size: {frame.shape}")
            cap.release()
    else:
        print("\n❌ No working cameras found")
        print("Check:")
        print("- Camera is connected")
        print("- Camera drivers are installed")
        print("- Camera is not used by another application")

if __name__ == "__main__":
    main()