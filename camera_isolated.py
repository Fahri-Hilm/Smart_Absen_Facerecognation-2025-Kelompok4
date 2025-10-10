#!/usr/bin/env python3
"""
Isolated camera process for face recognition attendance
This script runs in a separate process to avoid GUI conflicts
"""

import cv2
import time
import sys
import os
import pickle
import joblib  # Add joblib for loading model
import numpy as np
from datetime import datetime, date
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def force_camera_cleanup():
    """Aggressive camera cleanup"""
    try:
        # Kill any hanging camera processes
        subprocess.run(['pkill', '-f', 'gst-launch'], capture_output=True, timeout=2)
        subprocess.run(['pkill', '-f', 'v4l2'], capture_output=True, timeout=2)
    except:
        pass
    
    # OpenCV cleanup
    try:
        cv2.destroyAllWindows()
        for i in range(10):
            cv2.waitKey(1)
    except:
        pass

def load_face_recognition_model():
    """Load the trained face recognition model"""
    try:
        # Model saved with joblib, load with joblib
        return joblib.load('static/face_recognition_model.pkl')
    except Exception as e:
        logger.error(f"Failed to load face recognition model: {e}")
        return None

def identify_face(face_image):
    """Identify face using the trained model"""
    try:
        model = load_face_recognition_model()
        if model is None:
            return ['Unknown']
        
        # Ensure grayscale and correct format
        if len(face_image.shape) > 2:
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        
        # Resize to match training format
        face_resized = cv2.resize(face_image, (50, 50))
        face_flattened = face_resized.flatten().reshape(1, -1)
        
        # Predict
        prediction = model.predict(face_flattened)
        return prediction
    except Exception as e:
        logger.error(f"Face recognition error: {e}")
        return ['Unknown']

def update_attendance_in_db(name, mode):
    """Update attendance in database (simplified for isolated process)"""
    try:
        # Import here to avoid circular imports
        sys.path.append('/home/fj/Desktop/PROJECT/SOFTWARE PROJECT/Absenn')
        from database import DatabaseManager
        from models import Employee, Attendance
        
        db = DatabaseManager()
        db.connect()
        
        username = name.split('_')[0]
        userbagian = name.split('_')[1]
        current_time = datetime.now().time()
        today = date.today()
        
        # Get employee
        employee = Employee.get_employee_by_name_bagian(username, userbagian)
        if not employee:
            if Employee.add_employee(username, userbagian):
                employee = Employee.get_employee_by_name_bagian(username, userbagian)
            else:
                return {'success': False, 'message': 'Gagal menambah karyawan ke database'}
        
        # Check existing attendance
        existing_attendance = Attendance.get_attendance_by_employee_date(employee['id'], today)
        
        # Update attendance using same logic as app.py
        if mode == 'masuk':
            if existing_attendance and existing_attendance.get('jam_masuk'):
                return {
                    'success': False, 
                    'message': f'Absensi masuk sudah tercatat hari ini pada {existing_attendance["jam_masuk"]}'
                }
            success = Attendance.add_or_update_attendance(employee['id'], today, jam_masuk=current_time)
            activity_type = 'login'
        else:  # mode == 'pulang'
            if existing_attendance and existing_attendance.get('jam_pulang'):
                return {
                    'success': False, 
                    'message': f'Absensi keluar sudah tercatat hari ini pada {existing_attendance["jam_pulang"]}'
                }
            success = Attendance.add_or_update_attendance(employee['id'], today, jam_pulang=current_time)
            activity_type = 'logout'
        
        if success:
            logger.info(f"Attendance updated: {username} - {mode} at {current_time}")
            return {'success': True, 'message': f'Absensi {mode} berhasil dicatat'}
        else:
            logger.error(f"Gagal update attendance: {username} - {mode}")
            return {'success': False, 'message': f'Gagal menyimpan absensi {mode}'}
        
    except Exception as e:
        logger.error(f"Database update error: {e}")
        return {'success': False, 'message': f'Error database: {str(e)}'}

def run_isolated_camera(mode, camera_id=0):
    """Run camera in isolated process"""
    cap = None
    window_name = None
    
    try:
        print(f"Starting isolated camera for {mode} mode")
        logger.info(f"Starting isolated camera for {mode} mode with camera {camera_id}")
        
        # Super aggressive cleanup first
        force_camera_cleanup()
        time.sleep(2)
        
        # Open camera with retries
        for attempt in range(3):
            try:
                cap = cv2.VideoCapture(camera_id)
                if cap.isOpened():
                    break
                else:
                    cap.release()
                    time.sleep(1)
            except:
                time.sleep(1)
        
        if cap is None or not cap.isOpened():
            print(f"ERROR: Cannot open camera {camera_id}")
            return False
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Load face detector
        face_detector = cv2.CascadeClassifier('/home/fj/Desktop/PROJECT/SOFTWARE PROJECT/Absenn/assets/haarcascade_frontalface_default.xml')
        
        # Create window with unique name
        window_name = f"ISOLATED_CAMERA_{mode.upper()}_{int(time.time())}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)
        cv2.moveWindow(window_name, 100, 100)
        
        print(f"Camera window '{window_name}' created for {mode}")
        logger.info(f"Camera window '{window_name}' created for {mode}")
        
        frame_count = 0
        detection_counter = 0
        start_time = time.time()
        recognition_success = False
        
        print(f"Camera {mode} started - Position your face in front of camera")
        print("Press ESC to exit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Cannot read frame from camera")
                break
            
            frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            # Draw interface
            cv2.putText(frame, f'ISOLATED CAMERA - {mode.upper()}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f'Frame: {frame_count}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            if len(faces) > 0:
                detection_counter += 1
                
                # Draw rectangle around face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, 'Face Detected!', (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.putText(frame, f'Detection: {detection_counter}/30', (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Process face recognition after 30 detections
                if detection_counter >= 30:
                    face_region = gray[faces[0][1]:faces[0][1]+faces[0][3], 
                                      faces[0][0]:faces[0][0]+faces[0][2]]
                    face = cv2.resize(face_region, (50, 50))
                    
                    # Identify face
                    try:
                        user = identify_face(face)[0]
                        print(f"Face identified as: {user}")
                        logger.info(f"Face identified as: {user}")
                        
                        if user != 'Unknown':
                            # Update attendance
                            attendance_result = update_attendance_in_db(user, mode)
                            print(f"Attendance result: {attendance_result}")
                            logger.info(f"Attendance update result: {attendance_result}")
                            
                            if attendance_result.get('success', False):
                                recognition_success = True
                                cv2.putText(frame, f'SUCCESS! {mode.upper()}', (10, 120), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                cv2.putText(frame, f'User: {user}', (10, 150), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                                cv2.putText(frame, 'Data saved to database!', (10, 180), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                            else:
                                cv2.putText(frame, 'ATTENDANCE FAILED!', (10, 120), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                                cv2.putText(frame, attendance_result.get('message', '')[:40], (10, 150), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                        else:
                            cv2.putText(frame, 'FACE NOT RECOGNIZED!', (10, 120), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    except Exception as e:
                        print(f"Recognition error: {e}")
                        cv2.putText(frame, 'RECOGNITION ERROR!', (10, 120), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    
                    cv2.putText(frame, 'Window will close in 3 seconds', (10, 210), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                    
                    # Show final result for 3 seconds
                    for i in range(90):  # 3 seconds @ 30fps
                        cv2.imshow(window_name, frame)
                        cv2.waitKey(33)
                    break
            else:
                detection_counter = max(0, detection_counter - 1)
                cv2.putText(frame, 'Position face in front of camera', (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Timeout after 30 seconds
            if time.time() - start_time > 30:
                cv2.putText(frame, 'TIMEOUT - Try again', (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                break
            
            # Show frame
            cv2.imshow(window_name, frame)
            
            # Check for ESC key
            key = cv2.waitKey(30) & 0xFF
            if key == 27:  # ESC
                print("ESC pressed, exiting")
                break
        
        return recognition_success
        
    except Exception as e:
        print(f"Camera error: {e}")
        logger.error(f"Camera error: {e}")
        return False
        
    finally:
        # Cleanup
        if cap is not None:
            cap.release()
        
        if window_name:
            try:
                cv2.destroyWindow(window_name)
            except:
                pass
        
        cv2.destroyAllWindows()
        for i in range(10):
            cv2.waitKey(1)
        
        print(f"Camera {mode} cleanup completed")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python camera_isolated.py <mode> <camera_id>")
        sys.exit(1)
    
    mode = sys.argv[1]
    camera_id = int(sys.argv[2])
    
    success = run_isolated_camera(mode, camera_id)
    sys.exit(0 if success else 1)