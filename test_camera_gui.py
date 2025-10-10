#!/usr/bin/env python3
"""
Test script untuk debug kamera GUI
"""
import cv2
import time

def test_camera_gui():
    print("Testing camera GUI...")
    
    try:
        # Test buka kamera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("ERROR: Tidak bisa buka kamera")
            return False
        
        print("Camera opened successfully")
        
        # Set resolusi
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Test buat window
        window_name = "Test Camera GUI"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        print(f"Window '{window_name}' created")
        
        frame_count = 0
        start_time = time.time()
        
        while frame_count < 100:  # Test 100 frames
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Tidak bisa baca frame")
                break
            
            frame_count += 1
            
            # Tambahkan text ke frame
            cv2.putText(frame, f'Test Frame: {frame_count}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, 'Press ESC to exit', (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Tampilkan frame
            cv2.imshow(window_name, frame)
            
            # Check for ESC key
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("ESC pressed, exiting...")
                break
            
            # Auto exit after 10 seconds
            if time.time() - start_time > 10:
                print("Auto exit after 10 seconds")
                break
        
        print(f"Processed {frame_count} frames")
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            cap.release()
            cv2.destroyAllWindows()
            print("Cleanup completed")
        except:
            pass
    
    return True

if __name__ == "__main__":
    success = test_camera_gui()
    print(f"Test result: {'SUCCESS' if success else 'FAILED'}")