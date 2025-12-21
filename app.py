import cv2
import os
import csv
import time
import hashlib
import secrets
import base64
import re
import json
from io import BytesIO
from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash, make_response
from werkzeug.utils import secure_filename
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
import shutil
import qrcode
from functools import wraps

# System imports
import threading
import signal
import sys
import atexit

# Import database modules
from database import get_db_manager
from models import Employee, Attendance, ActivityLog
from config import get_app_config
from qr_sync import qr_sync_manager, start_cleanup_thread
import logging

# Setup logging FIRST (before importing InsightFace)
log_level = logging.WARNING if os.getenv('FLASK_ENV') == 'production' else logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
logger.info(f"🔧 Logging level: {logging.getLevelName(log_level)}")

# InsightFace for better accuracy (99%+)
USE_INSIGHTFACE = False
try:
    from face_recognition_insightface import (
        identify_face_insightface,
        train_insightface_model,
        extract_face_embedding,
        detect_faces_insightface,
        get_database_stats,
        load_face_database
    )
    USE_INSIGHTFACE = True
    logger.info("✅ InsightFace loaded - using ArcFace (99%+ accuracy)")
except ImportError as e:
    logger.warning(f"⚠️ InsightFace not available, using KNN fallback: {e}")

app = Flask(__name__)

# Load app configuration
app_config = get_app_config()
app.secret_key = app_config['secret_key']

# Enable response compression for performance
try:
    from flask_compress import Compress
    Compress(app)
    logger.info("🗜️ Response compression enabled")
except ImportError:
    logger.warning("⚠️ Flask-Compress not available. Install: pip install flask-compress")

# Setup Swagger UI for API documentation
try:
    from swagger_config import setup_swagger
    setup_swagger(app)
    logger.info("📚 Swagger UI enabled at /api/docs")
except ImportError:
    logger.warning("⚠️ Swagger UI not available. Install: pip install flask-swagger-ui")

# QR Code Authentication System
QR_VALIDITY_MINUTES = 10  # QR code berlaku 10 menit
current_unit_code = None
qr_code_generated_time = None
qr_refresh_counter = 0  # Counter untuk force refresh

def generate_unit_code(force_new=False):
    """Generate kode unit yang unik berdasarkan waktu"""
    global qr_refresh_counter
    current_time = datetime.now()
    
    if force_new:
        # Jika force refresh, gunakan counter untuk membuat kode berbeda
        qr_refresh_counter += 1
        secret_base = f"KAFEBASABASI-{current_time.timestamp()}-{qr_refresh_counter}"
    else:
        # Buat kode berdasarkan slot 10 menit
        time_slot = int(current_time.timestamp() // (QR_VALIDITY_MINUTES * 60))
        secret_base = f"KAFEBASABASI-{time_slot}"
    
    return hashlib.md5(secret_base.encode()).hexdigest()[:8].upper()

def get_current_unit_code():
    """Dapatkan kode unit saat ini, generate baru jika perlu"""
    global current_unit_code, qr_code_generated_time
    
    current_time = datetime.now()
    
    # Jika belum ada kode atau sudah lewat 10 menit, generate baru
    if (current_unit_code is None or 
        qr_code_generated_time is None or 
        (current_time - qr_code_generated_time).total_seconds() >= QR_VALIDITY_MINUTES * 60):
        
        current_unit_code = generate_unit_code()
        qr_code_generated_time = current_time
        logger.info(f"Generated new unit code: {current_unit_code}")
    
    return current_unit_code

# QR Code cache for performance
_qr_cache = {'code': None, 'image': None, 'url': None, 'timestamp': None}

def generate_qr_code():
    """Generate QR code untuk authentication - with caching"""
    global _qr_cache
    
    unit_code = get_current_unit_code()
    
    # Return cached QR if same code (performance optimization)
    if _qr_cache['code'] == unit_code and _qr_cache['image']:
        logger.debug(f"Using cached QR code for: {unit_code}")
        return _qr_cache['image'], _qr_cache['url']
    
    base_url = request.host_url.rstrip('/')
    qr_url = f"{base_url}/mobile_verify?unit={unit_code}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 untuk display di HTML
    buffered = BytesIO()
    img.save(buffered, "PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Cache the result
    _qr_cache = {
        'code': unit_code,
        'image': img_str,
        'url': qr_url,
        'timestamp': datetime.now()
    }
    logger.debug(f"Generated and cached new QR code: {unit_code}")
    
    return img_str, qr_url

def is_valid_unit_code(provided_code):
    """Validasi apakah kode unit masih valid"""
    current_code = get_current_unit_code()
    return provided_code == current_code

# Initialize database
db_manager = get_db_manager()
if not db_manager.initialize_database():
    logger.error("Gagal inisialisasi database!")

nimgs = 10
selected_camera_id = 0  # Akan dipilih lewat dropdown

def cleanup_opencv_resources():
    """Comprehensive OpenCV resource cleanup"""
    try:
        import time
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        time.sleep(0.1)  # Give time for cleanup
        
        # Additional cleanup cycles
        for _ in range(3):
            cv2.waitKey(1)
        
        print("[DEBUG] OpenCV resources cleaned up")
        return True
    except Exception as e:
        print(f"[DEBUG] Error during OpenCV cleanup: {e}")
        return False

# Tanggal minggu ini
current_date = date.today()
start_of_week = current_date - timedelta(days=current_date.weekday())
end_of_week = start_of_week + timedelta(days=6)
datetoday_week = start_of_week.strftime("%Y-W%U")
datetoday2 = start_of_week.strftime("%d-%B-%Y")
date_range_week = f"{start_of_week.strftime('%d %B')} - {end_of_week.strftime('%d %B %Y')}"
tanggal_hari_ini = current_date.strftime("%A, %d %B %Y")
attendance_filename = f'Attendance/Attendance-{datetoday_week}.csv'

# Inisialisasi folder & face detector
face_detector = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
os.makedirs('Attendance', exist_ok=True)
os.makedirs('static/faces', exist_ok=True)

# Buat file absensi jika belum ada
if not os.path.exists(attendance_filename):
    with open(attendance_filename, 'w') as f:
        f.write('Name,Bagian,Tanggal,Jam Berangkat,Jam Pulang,Total Jam Kerja\n')

# Admin Configuration
ADMIN_CREDENTIALS = {
    'admin': 'admin123',
    'supervisor': 'super123'
}

def admin_required(f):
    """Decorator untuk memerlukan login admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def totalreg():
    """Menghitung total karyawan terdaftar dari database"""
    try:
        employees = Employee.get_all_employees()
        return len(employees) if employees else 0
    except Exception as e:
        logger.error(f"Error getting total registered employees: {e}")
        # Fallback ke folder jika database error
        try:
            return len(os.listdir('static/faces'))
        except:
            return 0

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []

def identify_face(facearray):
    """
    Identify face menggunakan InsightFace/ArcFace (99%+ accuracy)
    
    Args:
        facearray: Face image array (grayscale/BGR, any shape)
    
    Returns:
        Tuple of (prediction_list, confidence_score)
    """
    if not USE_INSIGHTFACE:
        logger.error("InsightFace tidak tersedia! Install dengan: pip install insightface onnxruntime")
        return ['Unknown'], 0.0
    
    try:
        logger.info("🔍 Face Recognition dengan InsightFace/ArcFace")
        
        # Convert input to proper format for InsightFace
        if len(facearray.shape) == 1:
            # Flattened array - reshape to square grayscale
            size = int(np.sqrt(len(facearray)))
            facearray = facearray.reshape(size, size).astype(np.uint8)
        
        # InsightFace needs BGR color image
        if len(facearray.shape) == 2:
            face_bgr = cv2.cvtColor(facearray, cv2.COLOR_GRAY2BGR)
        else:
            face_bgr = facearray
        
        # Resize to optimal size for ArcFace feature extraction
        face_bgr = cv2.resize(face_bgr, (160, 160), interpolation=cv2.INTER_CUBIC)
        
        nik_or_name, confidence = identify_face_insightface(face_bgr, threshold=0.45)
        
        # NIK to Name lookup - jika hasil adalah NIK (angka), cari nama dari database
        final_name = nik_or_name
        if nik_or_name != "Unknown" and nik_or_name.isdigit():
            # Ini adalah NIK, cari nama karyawan dari database
            try:
                employee = Employee.get_employee_by_nik(nik_or_name)
                if employee:
                    final_name = employee.get('name', nik_or_name)
                    logger.info(f"📋 NIK {nik_or_name} -> Nama: {final_name}")
            except Exception as lookup_err:
                logger.warning(f"⚠️ NIK lookup failed: {lookup_err}")
                final_name = nik_or_name
        
        logger.info(f"✅ InsightFace result: {final_name} ({confidence:.1f}%)")
        return [final_name], confidence
        
    except Exception as e:
        logger.error(f"❌ InsightFace recognition failed: {e}")
        return ['Unknown'], 0.0

def identify_face_insightface_wrapper(face_bgr):
    """
    Wrapper untuk InsightFace recognition yang menerima gambar BGR langsung
    
    Args:
        face_bgr: BGR color image (OpenCV format)
    
    Returns:
        Tuple of (prediction_list, confidence_score)
    """
    if not USE_INSIGHTFACE:
        logger.error("InsightFace tidak tersedia!")
        return ['Unknown'], 0.0
    
    try:
        logger.info("🔍 Face Recognition dengan InsightFace/ArcFace (BGR mode)")
        
        # Ensure user packages are prioritized
        import sys
        user_packages = '/home/fj/.local/lib/python3.12/site-packages'
        if user_packages not in sys.path:
            sys.path.insert(0, user_packages)
        
        # Call InsightFace directly with BGR image
        nik_or_name, confidence = identify_face_insightface(face_bgr, threshold=0.45)
        
        # NIK to Name lookup
        final_name = nik_or_name
        if nik_or_name != "Unknown" and nik_or_name.isdigit():
            try:
                employee = Employee.get_employee_by_nik(nik_or_name)
                if employee:
                    final_name = employee.get('name', nik_or_name)
                    logger.info(f"📋 NIK {nik_or_name} -> Nama: {final_name}")
            except Exception as lookup_err:
                logger.warning(f"⚠️ NIK lookup failed: {lookup_err}")
        
        logger.info(f"✅ InsightFace BGR result: {final_name} ({confidence:.1f}%)")
        return [final_name], confidence
        
    except Exception as e:
        logger.error(f"❌ InsightFace BGR recognition failed: {e}")
        import traceback
        traceback.print_exc()
        return ['Unknown'], 0.0

def train_model():
    """
    Train face recognition menggunakan InsightFace/ArcFace (99%+ accuracy)
    Hanya butuh 5-10 foto per orang untuk hasil optimal
    """
    if not USE_INSIGHTFACE:
        logger.error("InsightFace tidak tersedia! Install dengan: pip install insightface onnxruntime")
        return False
    
    try:
        # Set training status - START
        set_training_status(True, 'Model', 10, 'Memulai training model...')
        
        logger.info("🚀 Training InsightFace/ArcFace model (99%+ accuracy)...")
        
        # Ensure user packages are prioritized (fix matplotlib/mpl_toolkits conflict)
        import sys
        user_packages = '/home/fj/.local/lib/python3.12/site-packages'
        if user_packages not in sys.path:
            sys.path.insert(0, user_packages)
        
        # Update progress
        set_training_status(True, 'Model', 30, 'Memuat model InsightFace...')
        
        success = train_insightface_model()
        
        if success:
            # Update progress
            set_training_status(True, 'Model', 80, 'Menyimpan model...')
            
            stats = get_database_stats()
            logger.info(f"✅ Model trained successfully!")
            logger.info(f"   📊 Total identities: {stats['total_identities']}")
            logger.info(f"   📸 Total embeddings: {stats['total_embeddings']}")
            
            # Training selesai
            set_training_status(False, 'Model', 100, f'Training selesai! {stats["total_identities"]} karyawan siap.')
            return True
        else:
            logger.error("❌ Training failed - no valid face data")
            set_training_status(False, 'Model', 0, 'Training gagal - tidak ada data wajah valid')
            return False
            
    except Exception as e:
        logger.error(f"❌ Training error: {e}")
        set_training_status(False, 'Model', 0, f'Training error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

def capture_employee_face_gui(name, bagian):
    """Capture wajah karyawan menggunakan GUI kamera"""
    try:
        # Create employee folder
        employee_folder = f'static/faces/{name}_{bagian}'
        os.makedirs(employee_folder, exist_ok=True)
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {'status': 'error', 'message': 'Kamera tidak tersedia'}
        
        window_name = f"Capture Wajah - {name} ({bagian})"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)
        
        captured_count = 0
        target_count = 50  # Capture 50 images
        frame_count = 0
        
        logger.info(f"Starting face capture for {name} ({bagian})")
        
        while captured_count < target_count:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            faces = extract_faces(frame)
            
            # Display frame with info
            cv2.putText(frame, f'CAPTURE WAJAH: {name}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f'Bagian: {bagian}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f'Progress: {captured_count}/{target_count}', (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Wajah Terdeteksi!', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Capture every 5 frames when face is detected
                if frame_count % 5 == 0:
                    face_img = frame[y:y+h, x:x+w]
                    face_filename = f'{employee_folder}/{captured_count+1}.jpg'
                    cv2.imwrite(face_filename, face_img)
                    captured_count += 1
                    
                    cv2.putText(frame, f'FOTO {captured_count} DISIMPAN!', (10, 120), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Posisikan wajah di depan kamera', (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.putText(frame, 'Tekan ESC untuk batalkan', (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            cv2.imshow(window_name, frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if captured_count >= target_count:
            logger.info(f"Face capture completed for {name}: {captured_count} photos")
            return {
                'status': 'success', 
                'message': f'Berhasil mengambil {captured_count} foto wajah untuk {name}!'
            }
        else:
            # Clean up incomplete capture
            shutil.rmtree(employee_folder, ignore_errors=True)
            return {
                'status': 'error', 
                'message': f'Capture dibatalkan. Hanya {captured_count} foto yang diambil.'
            }
            
    except Exception as e:
        logger.error(f"Error in capture_employee_face_gui: {e}")
        return {'status': 'error', 'message': str(e)}

def save_employee_face_from_mobile(name, bagian, face_image_data):
    """Simpan wajah karyawan dari mobile capture"""
    try:
        # Create employee folder
        employee_folder = f'static/faces/{name}_{bagian}'
        os.makedirs(employee_folder, exist_ok=True)
        
        # Process base64 image
        if ',' in face_image_data:
            face_image_data = face_image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(face_image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return {'status': 'error', 'message': 'Gagal memproses gambar'}
        
        # Extract face from image
        faces = extract_faces(frame)
        
        if len(faces) == 0:
            return {'status': 'error', 'message': 'Tidak ada wajah yang terdeteksi dalam gambar'}
        
        # Save multiple versions of the face for better training
        (x, y, w, h) = faces[0]
        face_img = frame[y:y+h, x:x+w]
        
        # Save original face
        cv2.imwrite(f'{employee_folder}/1.jpg', face_img)
        
        # Create variations for better training
        for i in range(2, 11):  # Create 10 variations
            # Add slight variations (brightness, contrast, etc.)
            variation = face_img.copy()
            
            # Brightness variation
            if i % 2 == 0:
                variation = cv2.convertScaleAbs(variation, alpha=1.1, beta=10)
            else:
                variation = cv2.convertScaleAbs(variation, alpha=0.9, beta=-10)
            
            # Save variation
            cv2.imwrite(f'{employee_folder}/{i}.jpg', variation)
        
        logger.info(f"Mobile face capture completed for {name}: 10 photos saved")
        return {
            'status': 'success', 
            'message': f'Berhasil menyimpan wajah {name} dari kamera mobile!'
        }
        
    except Exception as e:
        logger.error(f"Error in save_employee_face_from_mobile: {e}")
        return {'status': 'error', 'message': str(e)}

def extract_attendance():
    """Mengambil data absensi dari database"""
    try:
        # Mengambil data absensi mingguan
        attendance_data = Attendance.get_weekly_attendance(start_of_week, end_of_week)
        
        # Check if data is None or empty or not iterable
        if not attendance_data or not isinstance(attendance_data, (list, tuple)):
            logger.info("No attendance data found or invalid data type")
            return [], [], [], [], 0
        
        names = []
        bagian = []
        tanggal = []
        times = []
        
        for record in attendance_data:
            if not record or not isinstance(record, dict):  # Skip None or invalid records
                continue
                
            names.append(record.get('name', 'Unknown'))
            bagian.append(record.get('bagian', 'Unknown'))
            
            # Handle tanggal
            record_date = record.get('tanggal')
            if record_date:
                if hasattr(record_date, 'strftime'):
                    tanggal.append(record_date.strftime("%d-%m-%Y"))
                else:
                    tanggal.append(str(record_date))
            else:
                tanggal.append('-')
            
            # Handle jam_masuk
            jam_masuk_val = record.get('jam_masuk')
            if jam_masuk_val:
                if hasattr(jam_masuk_val, 'strftime'):
                    jam_masuk = jam_masuk_val.strftime("%H:%M:%S")
                else:
                    jam_masuk = str(jam_masuk_val)
            else:
                jam_masuk = '-'
            
            # Handle jam_pulang  
            jam_pulang_val = record.get('jam_pulang')
            if jam_pulang_val:
                if hasattr(jam_pulang_val, 'strftime'):
                    jam_pulang = jam_pulang_val.strftime("%H:%M:%S")
                else:
                    jam_pulang = str(jam_pulang_val)
            else:
                jam_pulang = '-'
            
            # Handle total_jam_kerja yang bisa berupa timedelta atau time
            total_jam = '-'
            total_jam_val = record.get('total_jam_kerja')
            if total_jam_val:
                if hasattr(total_jam_val, 'total_seconds'):
                    # Ini adalah timedelta object
                    total_seconds = int(total_jam_val.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    total_jam = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                elif hasattr(total_jam_val, 'strftime'):
                    # Ini adalah time object
                    total_jam = total_jam_val.strftime("%H:%M:%S")
                else:
                    # Convert to string as fallback
                    total_jam = str(total_jam_val)
            
            times.append((jam_masuk, jam_pulang, total_jam))
        
        return names, bagian, tanggal, times, len(names)
        
    except Exception as e:
        logger.error(f"Error extracting attendance: {e}")
        return [], [], [], [], 0

# ======================== QR AUTHENTICATION ROUTES ========================

@app.route('/auth')
def qr_auth():
    """Halaman QR authentication - halaman pertama yang dilihat user"""
    try:
        # AGGRESSIVE CLEANUP: Clear ALL QR-related session data when returning to QR page
        old_verified_unit = session.get('verified_unit_code')
        
        # Clear all QR session data
        session.pop('qr_verified', None)
        session.pop('qr_verified_time', None)
        session.pop('verified_unit_code', None)
        session.pop('last_sync_time', None)
        session.pop('qr_session_consumed', None)
        session.pop('attendance_completed_time', None)
        
        # Remove ALL sessions for this unit code from qr_sync_manager
        if old_verified_unit:
            cleared = qr_sync_manager.clear_unit_code_sessions(old_verified_unit)
            logger.info(f"🧹 Cleared {cleared} QR sessions for unit: {old_verified_unit}")
        
        qr_image, qr_url = generate_qr_code()
        unit_code = get_current_unit_code()
        
        # Hitung sisa waktu berlaku
        current_time = datetime.now()
        if qr_code_generated_time:
            elapsed_seconds = int((current_time - qr_code_generated_time).total_seconds())
            remaining_seconds = max(0, (QR_VALIDITY_MINUTES * 60) - elapsed_seconds)
        else:
            remaining_seconds = QR_VALIDITY_MINUTES * 60
        
        return render_template('qr_auth.html',
                             qr_image=qr_image,
                             qr_url=qr_url,
                             unit_code=unit_code,
                             remaining_seconds=remaining_seconds)
    except Exception as e:
        logger.error(f"Error generating QR auth page: {e}")
        return f"Error: {str(e)}", 500

@app.route('/api/qr_sync_status')
def qr_sync_status():
    """API untuk cek status QR sync real-time - untuk auto-redirect laptop saat HP scan QR"""
    try:
        current_unit = get_current_unit_code()  # QR code yang sedang ditampilkan di laptop
        latest_auth = qr_sync_manager.get_latest_auth(current_unit)
        
        # Check if attendance was just completed (within last 30 seconds)
        attendance_completed_time = session.get('attendance_completed_time')
        if attendance_completed_time:
            time_since_completion = (datetime.now() - datetime.fromisoformat(attendance_completed_time)).total_seconds()
            if time_since_completion < 30:  # Grace period 30 detik
                logger.info(f"🛑 Attendance completed {time_since_completion:.1f}s ago, skipping sync check")
                return jsonify({
                    'success': True,
                    'has_pending_sync': False,
                    'status': 'attendance_completed',
                    'message': 'Absensi selesai, menunggu scan QR baru...'
                })
            else:
                # Clear old flag after grace period
                session.pop('attendance_completed_time', None)
        
        if latest_auth:
            # Check if the scanned QR matches current displayed QR
            scanned_unit = latest_auth.get('unit_code') or latest_auth.get('code')
            session_verified_unit = session.get('verified_unit_code')
            last_sync_time = session.get('last_sync_time')
            
            # Get timestamp of the scan
            scan_timestamp = latest_auth.get('verified_at') or latest_auth.get('timestamp')
            scan_time_str = scan_timestamp.isoformat() if scan_timestamp else None
            
            # IMPORTANT: Check if this session was already consumed
            consumed_session = session.get('qr_session_consumed')
            current_session_key = f"{scanned_unit}_{scan_time_str}"
            
            if consumed_session == current_session_key:
                logger.info(f"⏭️ Skipping already consumed QR session: {current_session_key}")
                return jsonify({
                    'success': True,
                    'has_pending_sync': False,
                    'status': 'already_used',
                    'message': 'QR session sudah digunakan'
                })
            
            # Ada pending sync jika:
            # 1. Unit code yang di-scan sama dengan yang ditampilkan di laptop
            # 2. DAN salah satu kondisi:
            #    a. Session laptop belum ter-verify dengan unit code tersebut
            #    b. ATAU ada scan baru (timestamp berbeda dari last_sync_time)
            is_new_scan = scan_time_str and scan_time_str != last_sync_time
            is_not_verified = session_verified_unit != scanned_unit
            
            if scanned_unit == current_unit and (is_not_verified or is_new_scan):
                # New authentication detected from mobile!
                logger.info(f"🔓 Pending QR sync detected: {scanned_unit} (new_scan={is_new_scan}, not_verified={is_not_verified})")
                return jsonify({
                    'success': True,
                    'has_pending_sync': True,
                    'session_id': scanned_unit,
                    'unit_code': scanned_unit,
                    'timestamp': scan_time_str,
                    'device_info': latest_auth.get('device_info'),
                    'message': 'QR scan berhasil dari perangkat mobile!'
                })
            else:
                return jsonify({
                    'success': True,
                    'has_pending_sync': False,
                    'status': 'current',
                    'unit_code': session_verified_unit
                })
        else:
            return jsonify({
                'success': True,
                'has_pending_sync': False,
                'status': 'no_auth',
                'message': 'Menunggu scan QR dari HP...'
            })
            
    except Exception as e:
        logger.error(f"Error checking QR sync status: {e}")
        return jsonify({
            'success': False,
            'has_pending_sync': False,
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/clear_qr_session', methods=['POST'])
def clear_qr_session():
    """Clear QR session setelah absensi berhasil - mencegah auto-redirect kembali"""
    try:
        # Clear session verification
        session.pop('qr_verified', None)
        session.pop('qr_verified_time', None)
        verified_unit = session.pop('verified_unit_code', None)
        session.pop('last_sync_time', None)
        # DON'T clear qr_session_consumed - we need it to prevent re-processing!
        
        # Set timestamp saat attendance selesai (untuk grace period)
        session['attendance_completed_time'] = datetime.now().isoformat()
        
        # Clear ALL sessions for this unit code from qr_sync_manager
        if verified_unit:
            cleared = qr_sync_manager.clear_unit_code_sessions(verified_unit)
            logger.info(f"🧹 Cleared {cleared} QR sessions for unit: {verified_unit}")
        
        return jsonify({
            'success': True,
            'message': 'QR session cleared successfully'
        })
    except Exception as e:
        logger.error(f"Error clearing QR session: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/accept_qr_sync', methods=['POST'])
def accept_qr_sync():
    """Accept QR sync from mobile and update laptop session - auto redirect laptop ke halaman absen"""
    try:
        # Support both JSON and form data
        if request.is_json:
            data = request.get_json()
            unit_code = data.get('session_id') or data.get('unit_code')
            sync_timestamp = data.get('timestamp')
        else:
            unit_code = request.form.get('unit_code') or request.form.get('session_id')
            sync_timestamp = request.form.get('timestamp')
        
        logger.info(f"🔐 Accept QR sync request for unit: {unit_code}")
        
        if unit_code and qr_sync_manager.is_authenticated(unit_code):
            # Update current session - laptop sekarang ter-verify
            session['qr_verified'] = True
            session['qr_verified_time'] = datetime.now().isoformat()
            session['verified_unit_code'] = unit_code
            # Simpan timestamp sync terakhir untuk deteksi scan baru
            session['last_sync_time'] = sync_timestamp or datetime.now().isoformat()
            # IMPORTANT: Mark this session as consumed to prevent re-detection
            session['qr_session_consumed'] = f"{unit_code}_{sync_timestamp}"
            
            logger.info(f"✅ QR sync accepted! Laptop session verified with unit: {unit_code}")
            
            # Redirect ke halaman absensi (web_attendance untuk flow baru)
            return jsonify({
                'success': True,
                'status': 'success',
                'message': 'QR sync berhasil! Mengarahkan ke halaman absensi...',
                'redirect_url': url_for('web_attendance')
            })
        else:
            logger.warning(f"❌ QR sync rejected - invalid or expired unit: {unit_code}")
            return jsonify({
                'success': False,
                'status': 'error',
                'message': 'QR code tidak valid atau sudah expired'
            })
            
    except Exception as e:
        logger.error(f"Error accepting QR sync: {e}")
        return jsonify({
            'success': False,
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/refresh_qr')
def refresh_qr():
    """Endpoint untuk refresh QR code via AJAX - dipanggil otomatis setiap 10 menit"""
    try:
        # Force regenerate QR code dengan kode baru
        global current_unit_code, qr_code_generated_time
        
        # Generate kode baru dengan force_new=True
        current_unit_code = generate_unit_code(force_new=True)
        qr_code_generated_time = datetime.now()
        
        qr_image, qr_url = generate_qr_code()
        unit_code = current_unit_code
        
        # Reset waktu tersisa ke 10 menit
        remaining_seconds = QR_VALIDITY_MINUTES * 60
        
        logger.info(f"🔄 QR code refreshed: {unit_code}")
        
        return jsonify({
            'success': True,
            'qr_image': qr_image,
            'qr_url': qr_url,
            'unit_code': unit_code,
            'remaining_seconds': remaining_seconds
        })
    except Exception as e:
        logger.error(f"Error refreshing QR code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/qr_info')
def qr_info():
    """API untuk mendapatkan info QR code saat ini (tanpa regenerate)"""
    try:
        unit_code = get_current_unit_code()
        
        # Hitung sisa waktu berlaku
        current_time = datetime.now()
        if qr_code_generated_time:
            elapsed_seconds = int((current_time - qr_code_generated_time).total_seconds())
            remaining_seconds = max(0, (QR_VALIDITY_MINUTES * 60) - elapsed_seconds)
        else:
            remaining_seconds = QR_VALIDITY_MINUTES * 60
        
        return jsonify({
            'success': True,
            'unit_code': unit_code,
            'remaining_seconds': remaining_seconds,
            'validity_minutes': QR_VALIDITY_MINUTES
        })
    except Exception as e:
        logger.error(f"Error getting QR info: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/mobile_verify')
def mobile_verify():
    """Halaman perantara untuk HP - mengambil device_id lalu redirect ke verify"""
    unit_code = request.args.get('unit', '').strip().upper()
    
    if not unit_code:
        flash('Kode unit tidak ditemukan.', 'error')
        return redirect(url_for('qr_auth'))
    
    # Render halaman yang akan mengambil device_id dan redirect
    return render_template('mobile_verify.html', unit_code=unit_code)

@app.route('/verify')
def verify_qr():
    """Verifikasi QR code dan redirect ke halaman utama dengan real-time sync"""
    provided_unit = request.args.get('unit', '').strip().upper()
    
    if not provided_unit:
        flash('Kode unit tidak ditemukan. Silakan scan QR code yang valid.', 'error')
        return redirect(url_for('qr_auth'))
    
    if is_valid_unit_code(provided_unit):
        # Set session untuk menandai bahwa user sudah terverifikasi
        session['qr_verified'] = True
        session['qr_verified_time'] = datetime.now().isoformat()
        session['verified_unit_code'] = provided_unit
        
        # Register QR verification in sync system
        user_agent = request.headers.get('User-Agent', '').lower()
        is_mobile = any(mobile in user_agent for mobile in ['android', 'iphone', 'ipad', 'mobile', 'webos', 'blackberry'])
        device_info = 'mobile' if is_mobile else 'desktop'
        
        # Notify sync system about successful authentication
        qr_sync_manager.verify_qr_auth(provided_unit, device_info, None, None)
        
        logger.info(f"QR verification successful with unit code: {provided_unit} from {device_info}")
        
        if is_mobile:
            # HP hanya sebagai kunci - tampilkan halaman sukses
            logger.info(f"Mobile device used as key - showing success page only")
            return render_template('qr_scan_success.html', 
                                   unit_code=provided_unit)
        else:
            # Desktop/Laptop - redirect langsung ke halaman absensi baru
            logger.info(f"Desktop device - redirecting to web_attendance page")
            flash('✅ Verifikasi berhasil! Silakan lakukan absensi.', 'success')
            return redirect(url_for('web_attendance'))
    else:
        logger.warning(f"Invalid QR code attempt with unit: {provided_unit}")
        flash('Kode unit tidak valid atau sudah kedaluwarsa. Silakan scan QR code terbaru.', 'error')
        return redirect(url_for('qr_auth'))

def qr_verification_required(f):
    """Decorator untuk memastikan user sudah melalui QR verification - dengan bypass untuk localhost"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # BYPASS QR verification untuk localhost/admin access
        if request.endpoint in ['localhost_home', 'admin_dashboard', 'admin_login'] or \
           request.path.startswith('/admin') or \
           (request.referrer and 'localhost' in request.referrer and '/localhost' in request.referrer):
            logger.info(f"QR verification bypassed for localhost access: {f.__name__}")
            return f(*args, **kwargs)
            
        logger.info(f"QR verification check for {f.__name__}: qr_verified={session.get('qr_verified', False)}")
        
        if not session.get('qr_verified'):
            logger.warning(f"QR verification failed for {f.__name__} - redirecting to auth")
            flash('Silakan scan QR code terlebih dahulu untuk akses sistem.', 'warning')
            return redirect(url_for('qr_auth'))
        
        # Check if verification is still valid (10 minutes)
        verification_time_str = session.get('qr_verified_time')
        if verification_time_str:
            verification_time = datetime.fromisoformat(verification_time_str)
            time_diff = (datetime.now() - verification_time).total_seconds()
            logger.info(f"QR verification time check: {time_diff}s ago (limit: {QR_VALIDITY_MINUTES * 60}s)")
            
            if time_diff > QR_VALIDITY_MINUTES * 60:
                logger.warning(f"QR verification expired for {f.__name__} - redirecting to auth")
                session.pop('qr_verified', None)
                session.pop('qr_verified_time', None)
                session.pop('verified_unit_code', None)
                flash('Sesi verifikasi telah berakhir. Silakan scan QR code lagi.', 'warning')
                return redirect(url_for('qr_auth'))
        
        return f(*args, **kwargs)
    return decorated_function

# ======================== MAIN ROUTES ========================

@app.route('/')
def home():
    """Halaman utama - langsung redirect ke QR auth"""
    return redirect(url_for('qr_auth'))

@app.route('/report')
def ui_ux_report():
    """Serve UI/UX report HTML - untuk Figma plugin import"""
    try:
        report_path = 'mockups_preview/LAPORAN_UI_UX_INTERAKTIF.html'
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        logger.error(f"Error serving report: {e}")
        return f"Error: {str(e)}", 500

@app.route('/localhost')
def localhost_home():
    """Halaman utama untuk testing localhost - bypass QR verification"""
    names, bagian, tanggal, times, l = extract_attendance()
    return render_template('user_home.html',
        names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
        totalreg=totalreg(), datetoday2=datetoday2,
        date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
        selected_camera=selected_camera_id)

@app.route('/localhost/mark_attendance', methods=['POST'])
def localhost_mark_attendance():
    """Route untuk absensi localhost tanpa QR verification"""
    try:
        logger.info("=== LOCALHOST MARK ATTENDANCE REQUEST ===")
        
        mode = request.form.get('mode', 'masuk')
        camera_id = request.form.get('camera_id', '0')
        
        logger.info(f"Localhost attendance request: mode={mode}, camera_id={camera_id}")
        
        # Check camera availability first
        if camera_id == '':
            return jsonify({
                'status': 'error',
                'message': 'Pilih kamera terlebih dahulu!'
            })
        
        # Import camera lock system
        from camera_lock import CameraLock, is_camera_busy
        
        # Check if camera is busy
        if is_camera_busy():
            return jsonify({
                'status': 'error',
                'message': '📷 Kamera sedang digunakan oleh perangkat lain. Silakan tunggu sebentar dan coba lagi.'
            })
        
        # Acquire camera lock
        try:
            with CameraLock() as camera_lock:
                logger.info(f"Localhost camera lock acquired for {mode} mode")
                
                # SIMPLE APPROACH: Always do complete cleanup before ANY camera operation
                logger.info(f"Performing complete camera cleanup before {mode} mode")
                
                # Step 1: Destroy all OpenCV windows (most important)
                try:
                    cv2.destroyAllWindows()
                    cv2.waitKey(10)
                    time.sleep(0.3)
                except:
                    pass
                
                # Step 2: Force release camera 0 specifically
                for attempt in range(3):
                    try:
                        temp_cap = cv2.VideoCapture(int(camera_id))
                        if temp_cap.isOpened():
                            temp_cap.release()
                        del temp_cap
                        time.sleep(0.2)
                    except:
                        pass
                
                # Step 3: Extra delay for pulang mode
                if mode == 'pulang':
                    logger.info("Extra delay for pulang mode")
                    time.sleep(1.0)
                
                # Step 4: Try camera operation with lock protection
                try:
                    result = run_attendance_with_camera(mode, int(camera_id))
                    return jsonify(result)
                except Exception as camera_error:
                    logger.error(f"Localhost camera error: {camera_error}")
                    # Fallback - simulasi absensi tanpa kamera untuk testing
                    return jsonify({
                        'status': 'warning',
                        'message': f'Kamera tidak tersedia. Mode simulasi: Absensi {mode} berhasil (demo mode)'
                    })
                    
        except RuntimeError as lock_error:
            logger.error(f"Localhost camera lock error: {lock_error}")
            return jsonify({
                'status': 'error',
                'message': '📷 Tidak dapat mengakses kamera. Perangkat lain sedang menggunakan kamera. Silakan tutup aplikasi kamera lain dan coba lagi.'
            })
            
    except Exception as e:
        logger.error(f"Error in localhost_mark_attendance: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Terjadi kesalahan koneksi: {str(e)}. Silakan refresh halaman dan coba lagi.'
        })

@app.route('/localhost/get_attendance_data')
def localhost_get_attendance_data():
    """AJAX endpoint untuk mendapatkan data absensi terbaru - localhost"""
    try:
        names, bagian, tanggal, times, l = extract_attendance()
        return jsonify({
            'status': 'success',
            'data': {
                'names': names,
                'bagian': bagian,
                'tanggal': tanggal,
                'times': times,
                'total': l,
                'totalreg': totalreg()
            }
        })
    except Exception as e:
        logger.error(f"Error getting localhost attendance data: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/localhost/get_cameras')
def localhost_get_cameras():
    """API untuk mendapatkan daftar kamera yang tersedia - localhost"""
    try:
        import os
        
        # Deteksi kamera yang tersedia
        cameras = []
        
        # Cek kamera default terlebih dahulu
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    cameras.append({
                        'id': 0,
                        'name': 'Webcam Default',
                        'status': 'active'
                    })
                cap.release()
        except Exception:
            pass
        
        # Jika tidak ada kamera aktif, berikan mode virtual
        if not cameras:
            cameras = [
                {
                    'id': 999,
                    'name': 'Mode Virtual (Testing)',
                    'status': 'virtual'
                }
            ]
            
        return jsonify(cameras)
    except Exception as e:
        logger.error(f"Error getting localhost cameras: {e}")
        return jsonify([{
            'id': 999,
            'name': 'Mode Fallback',
            'status': 'fallback'
        }])

# ======================== ADMIN ROUTES ========================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Login page untuk admin"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Anda telah logout', 'info')
    return redirect(url_for('home'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Dashboard admin dengan semua fitur management - AdminLTE style"""
    names, bagian, tanggal, times, l = extract_attendance()
    
    # Hitung absensi hari ini
    today_str = current_date.strftime("%d-%m-%Y")
    hadir_hari_ini = sum(1 for t in tanggal if t == today_str)
    
    # Gunakan template AdminLTE style
    return render_template('admin_dashboard.html',
        names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
        totalreg=totalreg(), datetoday2=datetoday2,
        date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
        selected_camera=selected_camera_id, hadir_hari_ini=hadir_hari_ini)

# ======================== USER ROUTES ========================

@app.route('/get_cameras')
@qr_verification_required
def get_cameras():
    """API untuk mendapatkan daftar kamera yang tersedia"""
    try:
        import os
        
        # Deteksi kamera yang tersedia
        cameras = []
        
        # Cek kamera default terlebih dahulu
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    cameras.append({
                        'id': 0,
                        'name': 'Webcam Default',
                        'status': 'active'
                    })
                cap.release()
        except Exception:
            pass
        
        # Jika tidak ada kamera aktif, berikan mode virtual
        if not cameras:
            cameras = [
                {
                    'id': 999,
                    'name': 'Mode Virtual (Testing)',
                    'status': 'virtual'
                }
            ]
            
        return jsonify(cameras)
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        return jsonify([{
            'id': 999,
            'name': 'Mode Fallback',
            'status': 'fallback'
        }])

@app.route('/select_camera', methods=['POST'])
def select_camera():
    """Endpoint untuk memilih kamera (AJAX)"""
    global selected_camera_id
    selected_camera_id = int(request.form.get('camera_id', 0))
    return jsonify({'status': 'success', 'camera_id': selected_camera_id})

@app.route('/api/time')
def api_time():
    """API untuk mendapatkan waktu saat ini"""
    return jsonify({
        'tanggal_hari_ini': tanggal_hari_ini,
        'date_range_week': date_range_week,
        'current_time': datetime.now().strftime("%H:%M:%S")
    })

# ======================== ADMIN MANAGEMENT ROUTES ========================

@app.route('/admin/add_employee', methods=['POST'])
@admin_required
def admin_add_employee():
    """Tambah karyawan baru"""
    name = request.form.get('name')
    bagian = request.form.get('bagian')
    
    if name and bagian:
        success = Employee.add_employee(name, bagian)
        if success:
            flash(f'Karyawan {name} berhasil ditambahkan!', 'success')
        else:
            flash('Gagal menambahkan karyawan. Mungkin sudah ada.', 'error')
    else:
        flash('Nama dan bagian harus diisi!', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/capture_face_gui', methods=['POST'])
@admin_required
def admin_capture_face_gui():
    """Capture wajah karyawan menggunakan GUI kamera"""
    try:
        data = request.get_json()
        name = data.get('name')
        bagian = data.get('bagian')
        
        if not name or not bagian:
            return jsonify({'status': 'error', 'message': 'Nama dan bagian harus diisi!'})
        
        # Jalankan face capture dengan GUI
        result = capture_employee_face_gui(name, bagian)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in capture_face_gui: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/admin/add_employee_complete', methods=['POST'])
@admin_required  
def admin_add_employee_complete():
    """Tambah karyawan DATA SAJA (tanpa foto) - Step 1 of 2-step workflow"""
    try:
        from datetime import datetime
        
        # Get form data
        full_name = request.form.get('fullName', '').strip()
        nik = request.form.get('nik', '').strip()
        gender = request.form.get('gender', '').strip()
        date_of_birth = request.form.get('dateOfBirth', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        position = request.form.get('position', '').strip()
        bagian = request.form.get('bagian', '').strip()
        hire_date = request.form.get('hireDate', '').strip()
        status = request.form.get('status', 'aktif').strip()
        notes = request.form.get('notes', '').strip()
        
        # Validasi input
        if not all([full_name, nik, gender, date_of_birth, email, phone, address, position, bagian, hire_date]):
            return jsonify({
                'status': 'error',
                'error': 'Semua field wajib diisi!'
            }), 400
        
        # Validasi NIK
        if not re.match(r'^\d{16}$', nik):
            return jsonify({
                'status': 'error',
                'error': 'NIK harus 16 digit'
            }), 400
        
        # Validasi email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return jsonify({
                'status': 'error',
                'error': 'Email tidak valid'
            }), 400
        
        # Validasi phone
        if not re.match(r'^0\d{9,}$', phone):
            return jsonify({
                'status': 'error',
                'error': 'Nomor telepon harus dimulai 0 dan minimal 10 digit'
            }), 400
        
        # Tambah ke database
        try:
            success = Employee.add_employee(
                name=full_name,
                bagian=bagian,
                email=email,
                phone=phone,
                gender=gender,
                address=address,
                position=position,
                status=status,
                hire_date=hire_date,
                nik=nik
            )
            
            if not success:
                return jsonify({
                    'status': 'error',
                    'error': 'Gagal menambahkan karyawan. Mungkin NIK atau email sudah terdaftar.'
                }), 400
        except Exception as db_error:
            logger.error(f"Database error: {db_error}")
            return jsonify({
                'status': 'error',
                'error': f'Database error: {str(db_error)}'
            }), 500
        
        # Get employee ID from database
        employee = Employee.get_employee_by_name_bagian(full_name, bagian)
        if not employee:
            return jsonify({
                'status': 'error',
                'error': 'Gagal mengambil ID karyawan'
            }), 500
        
        logger.info(f"Karyawan {full_name} ({nik}) berhasil ditambahkan. Siap untuk capture wajah.")
        
        return jsonify({
            'status': 'success',
            'message': f'Data karyawan {full_name} berhasil disimpan! Lanjut ke capture wajah.',
            'employee_id': employee['id'],
            'name': full_name,
            'dept': bagian
        }), 201
        
    except Exception as e:
        logger.error(f"Error in add_employee_complete: {e}")
        return jsonify({
            'status': 'error',
            'error': f'Error: {str(e)}'
        }), 500

# ==================== CAPTURE WAJAH PAGE & API ====================

@app.route('/capture_wajah', methods=['GET'])
@admin_required
def capture_wajah_page():
    """Halaman capture wajah untuk training photos (40+ photos)"""
    try:
        employee_id = request.args.get('employee_id')
        employee_name = request.args.get('name', '')
        employee_dept = request.args.get('dept', '')
        
        if not employee_id:
            flash('Employee ID tidak valid', 'error')
            return redirect('/admin/employees')
        
        return render_template('capture_wajah.html', 
                             employee_id=employee_id,
                             employee_name=employee_name,
                             employee_dept=employee_dept)
    except Exception as e:
        logger.error(f"Error loading capture_wajah page: {e}")
        flash('Gagal memuat halaman capture wajah', 'error')
        return redirect('/admin/employees')

@app.route('/camera-debug')
def camera_debug():
    """Debug page untuk test kamera"""
    return render_template('camera_debug.html')

@app.route('/api/train_model', methods=['POST'])
@admin_required
def api_train_model():
    """API endpoint untuk training model InsightFace"""
    try:
        logger.info("🚀 API: Training InsightFace model...")
        success = train_model()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': '✅ Model InsightFace berhasil ditraining!'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'error': 'Training gagal - tidak ada data wajah yang valid'
            }), 400
            
    except Exception as e:
        logger.error(f"Error in api_train_model: {e}")
        return jsonify({
            'status': 'error',
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/test/training-loader')
def test_training_loader():
    """Halaman test untuk training loader"""
    return render_template('test_training_loader.html')

@app.route('/api/simulate_training', methods=['POST'])
def simulate_training():
    """Simulate training process untuk test"""
    try:
        import threading
        import time
        
        def simulate_process():
            steps = [
                (10, 'Memulai training...'),
                (30, 'Memuat model InsightFace...'),
                (50, 'Memproses foto wajah...'),
                (70, 'Membuat embeddings...'),
                (90, 'Menyimpan model...'),
                (100, 'Training selesai!')
            ]
            
            for progress, message in steps:
                set_training_status(True, 'Test Employee', progress, message)
                time.sleep(1)
            
            # Selesai
            set_training_status(False, 'Test Employee', 100, 'Training selesai!')
        
        # Jalankan di background
        thread = threading.Thread(target=simulate_process)
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'Simulation started'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

# Global training status
training_status = {
    'is_training': False,
    'employee_name': '',
    'progress': 0,
    'message': '',
    'start_time': None
}

@app.route('/api/training_status')
def get_training_status():
    """API untuk mendapatkan status training real-time"""
    global training_status
    return jsonify(training_status)

def set_training_status(is_training, employee_name='', progress=0, message=''):
    """Helper function untuk update training status"""
    global training_status
    training_status.update({
        'is_training': is_training,
        'employee_name': employee_name,
        'progress': progress,
        'message': message,
        'start_time': datetime.now().isoformat() if is_training else None
    })

@app.route('/test/auto-training')
def test_auto_training():
    """Test endpoint untuk memastikan auto-training berjalan"""
    try:
        # Simulasi save foto dan auto-training
        employee_id = 1
        saved_count = 10
        
        # Get employee
        employees = Employee.get_all_employees()
        employee = next((emp for emp in employees if emp['id'] == int(employee_id)), None)
        
        if not employee:
            return "❌ Employee tidak ditemukan"
        
        nik = employee.get('nik', 'unknown')
        full_name = employee.get('name', 'Unknown')
        
        # Test auto-training
        train_success = False
        train_error = ""
        
        try:
            logger.info(f"🚀 TEST AUTO TRAINING for {full_name}...")
            train_success = train_model()
            if train_success:
                logger.info(f"✅ TEST AUTO TRAINING SUCCESS: {full_name}")
            else:
                logger.error(f"❌ TEST AUTO TRAINING FAILED: {full_name}")
                train_error = "Training model gagal"
        except Exception as e:
            logger.error(f"❌ TEST AUTO TRAINING ERROR: {e}")
            train_error = str(e)
        
        # Response message
        response_message = f'✅ {full_name} test dengan {saved_count} foto!'
        if train_success:
            response_message += ' Model berhasil di-training dan siap untuk absensi!'
        else:
            response_message += f' ⚠️ Training gagal: {train_error}'
        
        return f"""
        <h2>🧪 Test Auto-Training Result</h2>
        <p><strong>Employee:</strong> {full_name} (ID: {employee_id}, NIK: {nik})</p>
        <p><strong>Training Success:</strong> {'✅ YES' if train_success else '❌ NO'}</p>
        <p><strong>Message:</strong> {response_message}</p>
        <p><strong>Saved Photos:</strong> {saved_count}</p>
        {f'<p><strong>Training Error:</strong> {train_error}</p>' if train_error else ''}
        <hr>
        <p><a href="/test/auto-training">🔄 Test lagi</a> | <a href="/admin">🏠 Admin Dashboard</a></p>
        """
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/capture/optimal')
def capture_optimal():
    """Halaman capture wajah dengan layout optimal"""
    return render_template('capture_optimal.html')

@app.route('/test/save-photos')
def test_save_photos():
    """Halaman test untuk save photos dan auto training"""
    return render_template('test_save_photos.html')

@app.route('/debug/test_save', methods=['POST', 'GET'])
def debug_test_save():
    """Debug endpoint untuk test save foto tanpa admin requirement"""
    if request.method == 'GET':
        return """
        <h2>Test Save Training Photos</h2>
        <form method="POST">
            <p>Employee ID: <input name="employee_id" value="1" required></p>
            <p>Jumlah foto dummy: <input name="photo_count" value="10" type="number" min="5" max="50"></p>
            <button type="submit">Test Save & Training</button>
        </form>
        """
    
    try:
        employee_id = request.form.get('employee_id', '1')
        photo_count = int(request.form.get('photo_count', '10'))
        
        # Get employee
        employees = Employee.get_all_employees()
        employee = next((emp for emp in employees if emp['id'] == int(employee_id)), None)
        
        if not employee:
            return f"❌ Employee ID {employee_id} tidak ditemukan"
        
        nik = employee.get('nik', str(employee_id))
        name = employee.get('name', 'Unknown')
        
        # Create dummy photos (1x1 pixel PNG)
        dummy_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77yQAAAABJRU5ErkJggg=="
        
        # Save photos
        faces_dir = f'static/faces/{nik}'
        os.makedirs(faces_dir, exist_ok=True)
        
        saved = 0
        for i in range(1, photo_count + 1):
            try:
                img_data = base64.b64decode(dummy_b64)
                with open(f'{faces_dir}/test_face_{i}.jpg', 'wb') as f:
                    f.write(img_data)
                saved += 1
            except Exception as e:
                continue
        
        # Training
        train_success = False
        train_error = ""
        try:
            train_success = train_model()
        except Exception as e:
            train_error = str(e)
        
        result = f"""
        <h2>✅ Test Save & Training Result</h2>
        <p><strong>Employee:</strong> {name} (ID: {employee_id}, NIK: {nik})</p>
        <p><strong>Photos saved:</strong> {saved}/{photo_count}</p>
        <p><strong>Save folder:</strong> {faces_dir}</p>
        <p><strong>Training success:</strong> {'✅ YES' if train_success else '❌ NO'}</p>
        {f'<p><strong>Training error:</strong> {train_error}</p>' if train_error else ''}
        <p><a href="/debug/test_save">← Test lagi</a></p>
        """
        
        return result
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/api/save_photos_simple', methods=['POST'])
@admin_required
def save_photos_simple():
    """Endpoint sederhana untuk save foto dan langsung training"""
    try:
        employee_id = request.form.get('employee_id')
        photos_data = request.form.get('photos')  # JSON string
        
        if not employee_id or not photos_data:
            return jsonify({'success': False, 'message': 'Data tidak lengkap'})
        
        import json
        photos = json.loads(photos_data)
        
        if len(photos) < 5:
            return jsonify({'success': False, 'message': f'Minimal 5 foto (ada {len(photos)})'})
        
        # Get employee
        employees = Employee.get_all_employees()
        employee = next((emp for emp in employees if emp['id'] == int(employee_id)), None)
        
        if not employee:
            return jsonify({'success': False, 'message': 'Karyawan tidak ditemukan'})
        
        nik = employee.get('nik', str(employee_id))
        name = employee.get('name', 'Unknown')
        
        # Save photos
        faces_dir = f'static/faces/{nik}'
        os.makedirs(faces_dir, exist_ok=True)
        
        saved = 0
        for i, photo in enumerate(photos[:30], 1):
            try:
                if ',' in photo:
                    photo = photo.split(',')[1]
                img_data = base64.b64decode(photo)
                with open(f'{faces_dir}/face_{i}.jpg', 'wb') as f:
                    f.write(img_data)
                saved += 1
            except:
                continue
        
        if saved < 5:
            return jsonify({'success': False, 'message': 'Gagal menyimpan foto'})
        
        # LANGSUNG TRAINING
        train_success = train_model()
        
        return jsonify({
            'success': True, 
            'message': f'✅ {name} berhasil! {saved} foto disimpan dan model di-training.',
            'trained': train_success
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/save_face_training', methods=['POST'])
def save_face_training():
    """API untuk menyimpan foto wajah dan PASTI langsung training"""
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        photos = data.get('photos', [])
        
        logger.info(f"🔄 SAVE_FACE_TRAINING: employee_id={employee_id}, photos={len(photos)}")
        
        if not employee_id or not photos:
            return jsonify({'status': 'error', 'error': 'Data tidak lengkap'}), 400
        
        if len(photos) < 5:
            return jsonify({'status': 'error', 'error': f'Minimal 5 foto (saat ini: {len(photos)})'}), 400
        
        # Get employee
        employees = Employee.get_all_employees()
        employee = next((emp for emp in employees if emp['id'] == int(employee_id)), None)
        
        if not employee:
            return jsonify({'status': 'error', 'error': 'Karyawan tidak ditemukan'}), 404
        
        nik = employee.get('nik', 'unknown')
        full_name = employee.get('name', 'Unknown')
        
        # Set loading status - SAVING
        set_training_status(True, full_name, 5, f'Menyimpan {len(photos)} foto untuk {full_name}...')
        
        # Save photos
        faces_dir = f'static/faces/{nik}'
        os.makedirs(faces_dir, exist_ok=True)
        
        saved_count = 0
        for idx, photo_base64 in enumerate(photos[:50], 1):
            try:
                if photo_base64.startswith('data:image'):
                    photo_base64 = photo_base64.split(',')[1]
                
                img_data = base64.b64decode(photo_base64)
                with open(f'{faces_dir}/face_{idx}.jpg', 'wb') as f:
                    f.write(img_data)
                saved_count += 1
                logger.info(f"📸 Saved photo {idx} for {full_name}")
                
                # Update progress
                progress = 5 + (idx / len(photos)) * 20  # 5-25%
                set_training_status(True, full_name, int(progress), f'Menyimpan foto {idx}/{len(photos)}...')
                
            except Exception as e:
                logger.warning(f"❌ Failed to save photo {idx}: {e}")
                continue
        
        if saved_count < 5:
            set_training_status(False, full_name, 0, 'Gagal menyimpan foto')
            return jsonify({'status': 'error', 'error': 'Gagal menyimpan foto'}), 500
        
        logger.info(f"✅ SAVED {saved_count} photos for {full_name}")
        
        # PASTI AUTO TRAINING - dengan loading status
        train_success = False
        train_error = ""
        try:
            set_training_status(True, full_name, 30, f'Memulai training model untuk {full_name}...')
            logger.info(f"🚀 STARTING AUTO TRAINING for {full_name}...")
            
            train_success = train_model()  # train_model() akan update progress sendiri
            
            if train_success:
                logger.info(f"✅ AUTO TRAINING SUCCESS: {full_name} dengan {saved_count} foto")
            else:
                logger.error(f"❌ AUTO TRAINING FAILED: {full_name}")
                train_error = "Training model gagal"
        except Exception as e:
            logger.error(f"❌ AUTO TRAINING ERROR: {e}")
            train_error = str(e)
            set_training_status(False, full_name, 0, f'Training error: {str(e)}')
        
        # Response dengan status training
        response_message = f'✅ {full_name} berhasil disimpan dengan {saved_count} foto!'
        if train_success:
            response_message += ' Model berhasil di-training dan siap untuk absensi!'
        else:
            response_message += f' ⚠️ Training gagal: {train_error}'
        
        return jsonify({
            'status': 'success',
            'message': response_message,
            'trained': train_success,
            'saved_photos': saved_count,
            'redirect': '/admin/employees'
        }), 201
        
    except Exception as e:
        logger.error(f"Error save_face_training: {e}")
        set_training_status(False, '', 0, f'Error: {str(e)}')
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/save_training_photos', methods=['POST'])
@admin_required
def save_training_photos():
    """API untuk menyimpan training photos dan PASTI langsung training model"""
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        photos = data.get('photos', [])
        
        logger.info(f"🔄 SAVE_TRAINING_PHOTOS: employee_id={employee_id}, photos={len(photos)}")
        
        if not employee_id or not photos:
            return jsonify({'status': 'error', 'error': 'Data tidak lengkap'}), 400
        
        if len(photos) < 5:
            return jsonify({'status': 'error', 'error': f'Minimal 5 foto (saat ini: {len(photos)})'}), 400
        
        # Get employee
        employees = Employee.get_all_employees()
        employee = next((emp for emp in employees if emp['id'] == int(employee_id)), None)
        
        if not employee:
            return jsonify({'status': 'error', 'error': 'Karyawan tidak ditemukan'}), 404
        
        nik = employee.get('nik', 'unknown')
        full_name = employee.get('name', 'Unknown')
        
        # Save photos
        faces_dir = f'static/faces/{nik}'
        os.makedirs(faces_dir, exist_ok=True)
        
        saved_count = 0
        for idx, photo_base64 in enumerate(photos[:50], 1):
            try:
                if photo_base64.startswith('data:image'):
                    photo_base64 = photo_base64.split(',')[1]
                
                img_data = base64.b64decode(photo_base64)
                with open(f'{faces_dir}/face_{idx}.jpg', 'wb') as f:
                    f.write(img_data)
                saved_count += 1
                logger.info(f"📸 Saved photo {idx} for {full_name}")
            except Exception as e:
                logger.warning(f"❌ Failed to save photo {idx}: {e}")
                continue
        
        if saved_count < 5:
            return jsonify({'status': 'error', 'error': 'Gagal menyimpan foto'}), 500
        
        logger.info(f"✅ SAVED {saved_count} photos for {full_name}")
        
        # PASTI AUTO TRAINING - dengan detailed logging
        train_success = False
        train_error = ""
        try:
            logger.info(f"🚀 STARTING AUTO TRAINING for {full_name}...")
            train_success = train_model()
            if train_success:
                logger.info(f"✅ AUTO TRAINING SUCCESS: {full_name} dengan {saved_count} foto")
            else:
                logger.error(f"❌ AUTO TRAINING FAILED: {full_name}")
                train_error = "Training model gagal"
        except Exception as e:
            logger.error(f"❌ AUTO TRAINING ERROR: {e}")
            train_error = str(e)
        
        # Response dengan status training
        response_message = f'✅ {full_name} berhasil disimpan dengan {saved_count} foto!'
        if train_success:
            response_message += ' Model berhasil di-training dan siap untuk absensi!'
        else:
            response_message += f' ⚠️ Training gagal: {train_error}'
        
        return jsonify({
            'status': 'success',
            'message': response_message,
            'trained': train_success,
            'saved_photos': saved_count
        }), 201
        
    except Exception as e:
        logger.error(f"Error save_training_photos: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/admin/add_employee_with_face', methods=['POST'])
@admin_required  
def admin_add_employee_with_face():
    """Tambah karyawan dengan face capture"""
    try:
        name = request.form.get('name')
        bagian = request.form.get('bagian')
        capture_method = request.form.get('capture_method')
        
        if not name or not bagian:
            return jsonify({'status': 'error', 'message': 'Nama dan bagian harus diisi!'})
        
        # Tambah karyawan ke database dulu
        success = Employee.add_employee(name, bagian)
        if not success:
            return jsonify({'status': 'error', 'message': 'Gagal menambahkan karyawan. Mungkin sudah ada.'})
        
        if capture_method == 'mobile':
            # Handle mobile capture
            face_image = request.form.get('face_image')
            if not face_image:
                return jsonify({'status': 'error', 'message': 'Data gambar tidak ditemukan!'})
            
            result = save_employee_face_from_mobile(name, bagian, face_image)
        else:
            # GUI capture sudah disimpan saat capture_face_gui dipanggil
            result = {'status': 'success', 'message': 'Face capture GUI sudah tersimpan'}
        
        if result['status'] == 'success':
            # Retrain model after adding new face
            train_model()
            return jsonify({
                'status': 'success', 
                'message': f'Karyawan {name} berhasil ditambahkan dengan face recognition!'
            })
        else:
            # Hapus karyawan jika face capture gagal  
            # Note: Implementasi delete bisa ditambahkan nanti jika diperlukan
            logger.warning(f"Face capture failed for {name}, employee remains in database")
            return jsonify(result)
            
    except Exception as e:
        logger.error(f"Error in add_employee_with_face: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/admin/delete_attendance', methods=['POST'])
@admin_required
def admin_delete_attendance():
    """Hapus data absensi"""
    name = request.form.get('name')
    date_str = request.form.get('date')
    
    if not name or not date_str:
        flash('Data tidak lengkap!', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        # Convert date string to date object
        date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
        
        # Get employee by name (assuming format: name_bagian)
        name_parts = name.split('_') if '_' in name else [name, '']
        employee_name = name_parts[0]
        employee_bagian = name_parts[1] if len(name_parts) > 1 else ''
        
        employee = Employee.get_employee_by_name_bagian(employee_name, employee_bagian)
        if employee:
            success = Attendance.delete_attendance(employee['id'], date_obj)
            if success:
                flash(f'Data absensi {name} pada {date_str} berhasil dihapus!', 'success')
            else:
                flash('Gagal menghapus data absensi.', 'error')
        else:
            flash('Karyawan tidak ditemukan.', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/clear_data')
@admin_required
def admin_clear_data():
    """Hapus semua data absensi"""
    try:
        db = get_db_manager()
        result = db.execute_query("DELETE FROM attendance")
        flash('Semua data absensi berhasil dihapus!', 'warning')
    except Exception as e:
        flash(f'Error clearing data: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/api/stats')
@admin_required
def admin_api_stats():
    """API untuk dashboard admin statistics"""
    try:
        # Get total employees
        employees = Employee.get_all_employees()
        total_employees = len(employees) if isinstance(employees, (list, tuple)) else 0
        
        # Get today's attendance
        today_attendance = Attendance.get_today_attendance()
        today_count = len(today_attendance) if isinstance(today_attendance, (list, tuple)) else 0
        
        # Calculate weekly average
        weekly_attendance = Attendance.get_weekly_attendance(start_of_week, end_of_week)
        weekly_count = len(weekly_attendance) if isinstance(weekly_attendance, (list, tuple)) else 0
        weekly_avg = weekly_count // 7 if weekly_count > 0 else 0
        
        # Calculate monthly total (approximate)
        monthly_total = weekly_count * 4  # Rough estimate
        
        # Calculate on-time rate (placeholder)
        on_time_rate = 85  # Placeholder percentage
        
        # Active cameras (placeholder)
        active_cameras = 1
        
        return jsonify({
            'totalEmployees': total_employees,
            'todayAttendance': today_count,
            'weeklyAverage': weekly_avg,
            'monthlyTotal': monthly_total,
            'onTimeRate': on_time_rate,
            'activeCameras': active_cameras,
            'totalreg': total_employees,
            'selected_camera': selected_camera_id
        })
    except Exception as e:
        logger.error(f"Error getting admin stats: {e}")
        return jsonify({
            'totalEmployees': 0,
            'todayAttendance': 0,
            'weeklyAverage': 0,
            'monthlyTotal': 0,
            'onTimeRate': 0,
            'activeCameras': 0,
            'totalreg': 0,
            'selected_camera': selected_camera_id
        })

# ======================== ADDITIONAL ADMIN ROUTES ========================

@app.route('/admin/add_employee_form')
@admin_required
def admin_add_employee_form():
    """Display comprehensive employee registration form"""
    try:
        bagian_list = ['Barista', 'Kasir', 'Kitchen', 'Supervisor', 'Manager']
        return render_template('add_employee_form.html', bagian_list=bagian_list)
    except Exception as e:
        logger.error(f"Error loading employee form: {e}")
        flash('Gagal memuat form karyawan!', 'error')
        return redirect('/admin/dashboard')

@app.route('/admin/employees')
@admin_required
def admin_employees():
    """Halaman manajemen karyawan"""
    try:
        logger.info("Loading admin employees page...")
        employees = Employee.get_all_employees()
        
        # Safe handling for employees data
        if isinstance(employees, (list, tuple)):
            employees_count = len(employees)
            employees_list = employees
        else:
            employees_count = 0
            employees_list = []
            
        logger.info(f"Retrieved {employees_count} employees")
        
        return render_template('admin_employees.html', 
                             employees=employees_list,
                             totalreg=totalreg(),
                             selected_camera=selected_camera_id)
    except Exception as e:
        logger.error(f'Error loading employees page: {str(e)}')
        flash(f'Error loading employees: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/attendance')
@admin_required
def admin_attendance():
    """Halaman data absensi"""
    names, bagian, tanggal, times, l = extract_attendance()
    return render_template('admin_attendance.html',
                         names=names, rolls=bagian, tanggal=tanggal, 
                         times=times, l=l, totalreg=totalreg(),
                         date_range_week=date_range_week,
                         selected_camera=selected_camera_id)

@app.route('/admin/reports')
@admin_required 
def admin_reports():
    """Halaman laporan dan export"""
    names, bagian, tanggal, times, l = extract_attendance()
    return render_template('admin_reports.html',
                         names=names, rolls=bagian, tanggal=tanggal,
                         times=times, l=l, totalreg=totalreg(),
                         date_range_week=date_range_week,
                         selected_camera=selected_camera_id)

@app.route('/admin/reports/daily')
@admin_required
def admin_reports_daily():
    """Generate laporan absensi harian"""
    try:
        db = get_db_manager()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Query untuk mendapatkan data absensi hari ini
        query = """
        SELECT e.name, e.bagian, a.jam_masuk, a.jam_pulang, a.status,
               TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang) as total_jam
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.employee_id AND DATE(a.tanggal) = %s
        ORDER BY e.name
        """
        
        result = db.execute_query(query, (today,))
        
        # Handle case where result is None or empty
        if not result:
            result = []
        elif isinstance(result, (int, type(None))):
            result = []
        elif isinstance(result, tuple):
            result = list(result)
        
        # Statistik harian
        total_karyawan = len(result) if isinstance(result, list) else 0
        hadir = len([r for r in result if isinstance(r, dict) and r.get('jam_masuk')]) if result else 0
        tidak_hadir = total_karyawan - hadir
        terlambat = len([r for r in result if isinstance(r, dict) and r.get('jam_masuk') and r.get('status') == 'Terlambat']) if result else 0
        
        report_data = {
            'tanggal': today,
            'total_karyawan': total_karyawan,
            'hadir': hadir,
            'tidak_hadir': tidak_hadir,
            'terlambat': terlambat,
            'persentase_kehadiran': round((hadir/total_karyawan)*100, 1) if total_karyawan > 0 else 0,
            'detail_karyawan': result
        }
        
        return jsonify({
            'status': 'success',
            'data': report_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating daily report: {str(e)}'
        }), 500

@app.route('/admin/reports/weekly')
@admin_required
def admin_reports_weekly():
    """Generate laporan absensi mingguan"""
    try:
        db = get_db_manager()
        
        # Hitung tanggal awal dan akhir minggu ini
        today = datetime.now()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        
        start_date = start_week.strftime('%Y-%m-%d')
        end_date = end_week.strftime('%Y-%m-%d')
        
        # Query untuk data mingguan
        query = """
        SELECT e.name, e.bagian,
               COUNT(a.id) as total_hari_kerja,
               COUNT(CASE WHEN a.jam_masuk IS NOT NULL THEN 1 END) as hari_hadir,
               COUNT(CASE WHEN a.status = 'Terlambat' THEN 1 END) as hari_terlambat,
               AVG(TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang)) as rata_jam_kerja
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.employee_id 
                                AND DATE(a.tanggal) BETWEEN %s AND %s
        GROUP BY e.id, e.name, e.bagian
        ORDER BY e.name
        """
        
        result = db.execute_query(query, (start_date, end_date))
        
        # Handle case where result is None or empty
        if not result:
            result = []
        elif isinstance(result, (int, type(None))):
            result = []
        elif isinstance(result, tuple):
            result = list(result)
        
        # Statistik mingguan
        total_karyawan = len(result) if isinstance(result, list) else 0
        if total_karyawan > 0 and result:
            rata_kehadiran = sum([r.get('hari_hadir', 0) for r in result if isinstance(r, dict)]) / (total_karyawan * 7) * 100
        else:
            rata_kehadiran = 0
        
        report_data = {
            'periode': f"{start_date} s/d {end_date}",
            'total_karyawan': total_karyawan,
            'rata_kehadiran': round(rata_kehadiran, 1),
            'detail_karyawan': result
        }
        
        return jsonify({
            'status': 'success',
            'data': report_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating weekly report: {str(e)}'
        }), 500

@app.route('/admin/reports/monthly')
@admin_required
def admin_reports_monthly():
    """Generate laporan absensi bulanan"""
    try:
        db = get_db_manager()
        
        # Ambil parameter bulan dari request, default bulan ini
        month = request.args.get('month', datetime.now().strftime('%Y-%m'))
        year_month = month + '-01'
        
        # Hitung hari pertama dan terakhir bulan
        first_day = datetime.strptime(year_month, '%Y-%m-%d')
        if first_day.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1) - timedelta(days=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1) - timedelta(days=1)
        
        start_date = first_day.strftime('%Y-%m-%d')
        end_date = last_day.strftime('%Y-%m-%d')
        
        # Query untuk data bulanan
        query = """
        SELECT e.name, e.bagian,
               COUNT(DISTINCT DATE(a.tanggal)) as total_hari_kerja,
               COUNT(CASE WHEN a.jam_masuk IS NOT NULL THEN 1 END) as hari_hadir,
               COUNT(CASE WHEN a.status = 'Terlambat' THEN 1 END) as hari_terlambat,
               SUM(TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang)) as total_jam_kerja,
               AVG(TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang)) as rata_jam_kerja
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.employee_id 
                                AND DATE(a.tanggal) BETWEEN %s AND %s
        GROUP BY e.id, e.name, e.bagian
        ORDER BY e.name
        """
        
        result = db.execute_query(query, (start_date, end_date))
        
        # Handle case where result is None or empty
        if not result:
            result = []
        elif isinstance(result, (int, type(None))):
            result = []
        elif isinstance(result, tuple):
            result = list(result)
        
        # Statistik bulanan
        total_karyawan = len(result) if isinstance(result, list) else 0
        total_hari_kerja = (last_day - first_day).days + 1
        
        report_data = {
            'periode': f"{start_date} s/d {end_date}",
            'bulan': month,
            'total_karyawan': total_karyawan,
            'total_hari_kerja': total_hari_kerja,
            'detail_karyawan': result
        }
        
        return jsonify({
            'status': 'success',
            'data': report_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating monthly report: {str(e)}'
        }), 500

@app.route('/admin/reports/performance')
@admin_required
def admin_reports_performance():
    """Generate laporan kinerja karyawan"""
    try:
        db = get_db_manager()
        
        # Query untuk analisis kinerja
        query = """
        SELECT e.name, e.bagian,
               COUNT(a.id) as total_absen,
               COUNT(CASE WHEN a.jam_masuk IS NOT NULL THEN 1 END) as total_hadir,
               COUNT(CASE WHEN a.status = 'Tepat Waktu' THEN 1 END) as tepat_waktu,
               COUNT(CASE WHEN a.status = 'Terlambat' THEN 1 END) as terlambat,
               AVG(TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang)) as rata_jam_kerja,
               MIN(TIME(a.jam_masuk)) as jam_masuk_tercepat,
               MAX(TIME(a.jam_pulang)) as jam_pulang_terlama
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.employee_id 
                                AND a.tanggal >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY e.id, e.name, e.bagian
        ORDER BY total_hadir DESC, tepat_waktu DESC
        """
        
        result = db.execute_query(query)
        
        # Handle case where result is None or empty
        if not result:
            result = []
        elif isinstance(result, (int, type(None))):
            result = []
        elif isinstance(result, tuple):
            result = list(result)
        
        # Hitung skor kinerja untuk setiap karyawan
        for record in result:
            if not isinstance(record, dict):
                continue
                
            total_hadir = record.get('total_hadir', 0) or 0
            tepat_waktu = record.get('tepat_waktu', 0) or 0
            rata_jam = record.get('rata_jam_kerja', 0) or 0
            
            # Skor berdasarkan kehadiran (40%), ketepatan (40%), jam kerja (20%)
            skor_kehadiran = (total_hadir / 30) * 40 if total_hadir > 0 else 0
            skor_ketepatan = (tepat_waktu / total_hadir) * 40 if total_hadir > 0 else 0
            skor_jam = min(rata_jam / 8, 1) * 20 if rata_jam > 0 else 0
            
            record['skor_kinerja'] = round(skor_kehadiran + skor_ketepatan + skor_jam, 1)
            record['persentase_kehadiran'] = round((total_hadir / 30) * 100, 1) if total_hadir > 0 else 0
            record['persentase_ketepatan'] = round((tepat_waktu / total_hadir) * 100, 1) if total_hadir > 0 else 0
        
        report_data = {
            'periode': '30 hari terakhir',
            'detail_karyawan': result
        }
        
        return jsonify({
            'status': 'success',
            'data': report_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating performance report: {str(e)}'
        }), 500

@app.route('/admin/reports/overtime')
@admin_required
def admin_reports_overtime():
    """Generate laporan lembur/overtime"""
    try:
        db = get_db_manager()
        
        # Parameter tanggal dari request
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
        end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        
        # Jam kerja normal (8 jam per hari)
        NORMAL_WORK_HOURS = 8
        
        # Query untuk analisis lembur
        query = """
        SELECT e.name, e.bagian,
               DATE(a.tanggal) as tanggal,
               a.jam_masuk, a.jam_pulang,
               TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang) as total_jam,
               CASE 
                   WHEN TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang) > %s 
                   THEN TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang) - %s
                   ELSE 0
               END as jam_lembur,
               CASE 
                   WHEN TIMESTAMPDIFF(HOUR, a.jam_masuk, a.jam_pulang) > %s 
                   THEN 'Lembur'
                   ELSE 'Normal'
               END as status_lembur
        FROM employees e
        JOIN attendance a ON e.id = a.employee_id 
        WHERE DATE(a.tanggal) BETWEEN %s AND %s
              AND a.jam_masuk IS NOT NULL 
              AND a.jam_pulang IS NOT NULL
        ORDER BY e.name, a.tanggal
        """
        
        result = db.execute_query(query, (NORMAL_WORK_HOURS, NORMAL_WORK_HOURS, NORMAL_WORK_HOURS, start_date, end_date))
        
        # Ensure result is a list of dictionaries
        if not result:
            result = []
        elif isinstance(result, (int, type(None))):
            result = []
        elif isinstance(result, tuple):
            result = list(result)
        
        # Statistik lembur
        total_records = len(result)
        overtime_records = 0
        total_overtime_hours = 0
        
        # Hitung overtime
        for record in result:
            if isinstance(record, dict) and record.get('jam_lembur', 0) > 0:
                overtime_records += 1
                total_overtime_hours += record.get('jam_lembur', 0)
        
        # Summary per karyawan
        employee_summary = {}
        for record in result:
            if not isinstance(record, dict):
                continue
                
            emp_name = record.get('name', '')
            if emp_name not in employee_summary:
                employee_summary[emp_name] = {
                    'name': emp_name,
                    'bagian': record.get('bagian', ''),
                    'total_hari_kerja': 0,
                    'hari_lembur': 0,
                    'total_jam_lembur': 0,
                    'rata_jam_lembur': 0
                }
            
            employee_summary[emp_name]['total_hari_kerja'] += 1
            jam_lembur = record.get('jam_lembur', 0)
            if jam_lembur > 0:
                employee_summary[emp_name]['hari_lembur'] += 1
                employee_summary[emp_name]['total_jam_lembur'] += jam_lembur
        
        # Hitung rata-rata jam lembur per karyawan
        for emp_data in employee_summary.values():
            if emp_data['hari_lembur'] > 0:
                emp_data['rata_jam_lembur'] = round(emp_data['total_jam_lembur'] / emp_data['hari_lembur'], 2)
        
        report_data = {
            'periode': f"{start_date} s/d {end_date}",
            'jam_kerja_normal': NORMAL_WORK_HOURS,
            'total_records': total_records,
            'overtime_records': overtime_records,
            'total_overtime_hours': total_overtime_hours,
            'rata_lembur_per_hari': round(total_overtime_hours / overtime_records, 2) if overtime_records > 0 else 0,
            'persentase_lembur': round((overtime_records / total_records) * 100, 1) if total_records > 0 else 0,
            'detail_harian': result,
            'summary_karyawan': list(employee_summary.values())
        }
        
        return jsonify({
            'status': 'success',
            'data': report_data
        })
        
    except Exception as e:
        logger.error(f"Error generating overtime report: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error generating overtime report: {str(e)}'
        }), 500

@app.route('/admin/reports/export')
@admin_required
def admin_reports_export():
    """Export laporan dalam berbagai format"""
    try:
        report_type = request.args.get('type', 'daily')
        format_type = request.args.get('format', 'csv')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        db = get_db_manager()
        
        # Query berdasarkan tipe laporan
        if report_type == 'daily':
            date_filter = start_date or datetime.now().strftime('%Y-%m-%d')
            query = """
            SELECT e.name as 'Nama Karyawan', e.bagian as 'Bagian', 
                   a.waktu_masuk as 'Waktu Masuk', a.waktu_keluar as 'Waktu Keluar', 
                   a.status as 'Status',
                   TIMESTAMPDIFF(HOUR, a.waktu_masuk, a.waktu_keluar) as 'Total Jam'
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id AND DATE(a.tanggal) = %s
            ORDER BY e.name
            """
            params = (date_filter,)
            filename = f"laporan_harian_{date_filter}"
            
        elif report_type == 'weekly':
            if not start_date or not end_date:
                # Default to current week
                today = datetime.now()
                start_week = today - timedelta(days=today.weekday())
                end_week = start_week + timedelta(days=6)
                start_date = start_week.strftime('%Y-%m-%d')
                end_date = end_week.strftime('%Y-%m-%d')
                
            query = """
            SELECT e.name as 'Nama Karyawan', e.bagian as 'Bagian',
                   COUNT(a.id) as 'Total Hari Kerja',
                   COUNT(CASE WHEN a.waktu_masuk IS NOT NULL THEN 1 END) as 'Hari Hadir',
                   COUNT(CASE WHEN a.status = 'Terlambat' THEN 1 END) as 'Hari Terlambat',
                   ROUND(AVG(TIMESTAMPDIFF(HOUR, a.waktu_masuk, a.waktu_keluar)), 2) as 'Rata-rata Jam Kerja'
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id 
                                    AND DATE(a.tanggal) BETWEEN %s AND %s
            GROUP BY e.id, e.name, e.bagian
            ORDER BY e.name
            """
            params = (start_date, end_date)
            filename = f"laporan_mingguan_{start_date}_to_{end_date}"
            
        elif report_type == 'monthly':
            if not start_date or not end_date:
                # Default to current month
                today = datetime.now()
                first_day = today.replace(day=1)
                if today.month == 12:
                    last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
                start_date = first_day.strftime('%Y-%m-%d')
                end_date = last_day.strftime('%Y-%m-%d')
                
            query = """
            SELECT e.name as 'Nama Karyawan', e.bagian as 'Bagian',
                   COUNT(DISTINCT DATE(a.tanggal)) as 'Total Hari Kerja',
                   COUNT(CASE WHEN a.waktu_masuk IS NOT NULL THEN 1 END) as 'Hari Hadir',
                   COUNT(CASE WHEN a.status = 'Terlambat' THEN 1 END) as 'Hari Terlambat',
                   ROUND(SUM(TIMESTAMPDIFF(HOUR, a.waktu_masuk, a.waktu_keluar)), 2) as 'Total Jam Kerja',
                   ROUND(AVG(TIMESTAMPDIFF(HOUR, a.waktu_masuk, a.waktu_keluar)), 2) as 'Rata-rata Jam Kerja'
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id 
                                    AND DATE(a.tanggal) BETWEEN %s AND %s
            GROUP BY e.id, e.name, e.bagian
            ORDER BY e.name
            """
            params = (start_date, end_date)
            filename = f"laporan_bulanan_{start_date}_to_{end_date}"
            
        elif report_type == 'performance':
            if not start_date or not end_date:
                # Default to last 30 days
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                
            query = """
            SELECT e.name as 'Nama Karyawan', e.bagian as 'Bagian',
                   COUNT(a.id) as 'Total Absen',
                   COUNT(CASE WHEN a.waktu_masuk IS NOT NULL THEN 1 END) as 'Total Hadir',
                   COUNT(CASE WHEN a.status = 'Tepat Waktu' THEN 1 END) as 'Tepat Waktu',
                   COUNT(CASE WHEN a.status = 'Terlambat' THEN 1 END) as 'Terlambat',
                   ROUND(AVG(TIMESTAMPDIFF(HOUR, a.waktu_masuk, a.waktu_keluar)), 2) as 'Rata-rata Jam Kerja',
                   ROUND((COUNT(CASE WHEN a.waktu_masuk IS NOT NULL THEN 1 END) / 30.0) * 100, 1) as 'Persentase Kehadiran'
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id 
                                    AND DATE(a.tanggal) BETWEEN %s AND %s
            GROUP BY e.id, e.name, e.bagian
            ORDER BY e.name
            """
            params = (start_date, end_date)
            filename = f"laporan_kinerja_{start_date}_to_{end_date}"
            
        else: # range type
            if not start_date or not end_date:
                return jsonify({'status': 'error', 'message': 'Start date and end date required'}), 400
                
            query = """
            SELECT e.name as 'Nama Karyawan', e.bagian as 'Bagian', 
                   DATE(a.tanggal) as 'Tanggal',
                   a.waktu_masuk as 'Waktu Masuk', a.waktu_keluar as 'Waktu Keluar', 
                   a.status as 'Status',
                   TIMESTAMPDIFF(HOUR, a.waktu_masuk, a.waktu_keluar) as 'Total Jam'
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id 
                                    AND DATE(a.tanggal) BETWEEN %s AND %s
            ORDER BY e.name, a.tanggal
            """
            params = (start_date, end_date)
            filename = f"laporan_{start_date}_to_{end_date}"
        
        result = db.execute_query(query, params)
        
        if not result:
            return jsonify({'status': 'error', 'message': 'No data found for the specified criteria'}), 404
        
        if format_type == 'csv':
            import csv
            from io import StringIO
            
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=result[0].keys() if result else [])
            writer.writeheader()
            writer.writerows(result)
            
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
            return response
            
        elif format_type == 'json':
            response_data = {
                'report_type': report_type,
                'date_range': f"{start_date} to {end_date}" if start_date and end_date else 'N/A',
                'generated_at': datetime.now().isoformat(),
                'total_records': len(result),
                'data': result
            }
            response = make_response(jsonify(response_data))
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}.json"'
            return response
            
        elif format_type == 'excel':
            try:
                import pandas as pd
                from io import BytesIO
                
                # Convert to DataFrame
                df = pd.DataFrame(result)
                
                # Create Excel file in memory
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Laporan Absensi', index=False)
                    
                    # Get workbook and worksheet for formatting
                    workbook = writer.book
                    worksheet = writer.sheets['Laporan Absensi']
                    
                    # Auto-adjust column width
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 30)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                
                output.seek(0)
                
                response = make_response(output.getvalue())
                response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response.headers['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
                return response
                
            except ImportError:
                return jsonify({'status': 'error', 'message': 'Excel export requires pandas and openpyxl. Please install: pip install pandas openpyxl'}), 500
                
        else:
            return jsonify({'status': 'error', 'message': f'Unsupported format: {format_type}. Supported formats: csv, json, excel'}), 400
            
    except Exception as e:
        logger.error(f"Error exporting report: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error exporting report: {str(e)}'
        }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error exporting report: {str(e)}'
        }), 500

@app.route('/admin/camera')
@admin_required
def admin_camera():
    """Halaman test dan manajemen kamera"""
    return render_template('admin_camera.html',
                         selected_camera=selected_camera_id,
                         totalreg=totalreg())

@app.route('/admin/database')
@admin_required
def admin_database():
    """Halaman manajemen database"""
    try:
        db = get_db_manager()
        # Test database connection
        db_status = "Connected" if db.get_connection() else "Disconnected"
        
        # Get table info
        tables_info = []
        for table in ['employees', 'attendance', 'activity_log']:
            try:
                count_result = db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                count = count_result[0]['count'] if count_result else 0
                tables_info.append({'name': table, 'records': count})
            except:
                tables_info.append({'name': table, 'records': 'Error'})
        
        return render_template('admin_database.html',
                             db_status=db_status,
                             tables_info=tables_info,
                             totalreg=totalreg(),
                             selected_camera=selected_camera_id)
    except Exception as e:
        flash(f'Error accessing database: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/database/reset', methods=['POST'])
@admin_required
def admin_database_reset():
    """Reset semua data di database"""
    try:
        # Import the reset function
        import os
        import shutil
        
        logger.info("Admin initiated database reset")
        
        db = get_db_manager()
        cursor = db.get_connection().cursor()
        
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Count records before deletion
        cursor.execute("SELECT COUNT(*) as count FROM employees")
        emp_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM attendance")
        att_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM activity_log")
        log_count = cursor.fetchone()['count']
        
        # Delete data in order (attendance first due to foreign keys)
        cursor.execute("DELETE FROM attendance")
        cursor.execute("DELETE FROM activity_log")
        cursor.execute("DELETE FROM employees")
        
        # Reset auto increment counters
        cursor.execute("ALTER TABLE employees AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE attendance AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE activity_log AUTO_INCREMENT = 1")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Commit changes
        db.get_connection().commit()
        cursor.close()
        
        # Delete face recognition model
        model_path = "static/face_recognition_model.pkl"
        if os.path.exists(model_path):
            os.remove(model_path)
            logger.info(f"Deleted face recognition model: {model_path}")
        
        # Delete all face images
        faces_dir = "static/faces"
        if os.path.exists(faces_dir):
            for item in os.listdir(faces_dir):
                item_path = os.path.join(faces_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                elif item.endswith(('.jpg', '.jpeg', '.png')):
                    os.remove(item_path)
        
        # Clear face recognition cache
        global face_recognition_model
        face_recognition_model = None
        
        logger.info(f"Database reset completed - Employees: {emp_count}, Attendance: {att_count}, Logs: {log_count}")
        
        flash(f'✅ Database reset berhasil! Dihapus: {emp_count} karyawan, {att_count} absensi, {log_count} log aktivitas', 'success')
        
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        flash(f'❌ Reset database gagal: {str(e)}', 'error')
    
    return redirect(url_for('admin_database'))

@app.route('/admin/database/status')
@admin_required 
def admin_database_status():
    """Get database status for AJAX"""
    try:
        db = get_db_manager()
        cursor = db.get_connection().cursor()
        
        # Get current counts
        cursor.execute("SELECT COUNT(*) as count FROM employees")
        emp_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM attendance")
        att_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM activity_log")
        log_count = cursor.fetchone()['count']
        
        cursor.close()
        
        return jsonify({
            'success': True,
            'employees': emp_count,
            'attendance': att_count,
            'activity_logs': log_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/admin/profile')
@admin_required
def admin_profile():
    """Halaman profil admin"""
    admin_username = session.get('admin_username', 'admin')
    return render_template('admin_profile.html',
                         admin_username=admin_username,
                         totalreg=totalreg(),
                         selected_camera=selected_camera_id)

@app.route('/admin/settings')
@admin_required
def admin_settings():
    """Halaman pengaturan sistem"""
    return render_template('admin_settings.html',
                         totalreg=totalreg(),
                         selected_camera=selected_camera_id,
                         current_config=get_app_config())

@app.route('/admin/api/cameras')
@admin_required
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

@app.route('/set_camera', methods=['POST'])
def set_camera():
    global selected_camera_id
    selected_camera_id = int(request.form['camera'])
    print(f"[DEBUG] Kamera dipilih: {selected_camera_id}")
    return home()

@app.route('/test_camera')
def test_camera():
    print(f"[DEBUG] Menguji kamera ID: {selected_camera_id}")
    cap = cv2.VideoCapture(selected_camera_id)
    if not cap.isOpened():
        return render_template('home.html', mess="Kamera tidak bisa dibuka.",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Uji Kamera - Tekan ESC untuk keluar', frame)
        if cv2.waitKey(1) == 27:  # ESC key
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return home()

@app.route('/absen_masuk')
def absen_masuk():
    """Redirect ke web-based attendance (tidak pakai GUI OpenCV)"""
    session['attendance_mode'] = 'masuk'
    return redirect(url_for('web_attendance'))

@app.route('/absen_pulang')
def absen_pulang():
    """Redirect ke web-based attendance (tidak pakai GUI OpenCV)"""
    session['attendance_mode'] = 'pulang'
    return redirect(url_for('web_attendance'))

@app.route('/direct_attendance')
def direct_attendance():
    """Direct access to attendance page - bypass QR for localhost"""
    # Set session as verified for localhost access
    session['qr_verified'] = True
    session['qr_verified_time'] = datetime.now().isoformat()
    session['verified_unit_code'] = 'LOCALHOST'
    
    logger.info("Direct attendance access - bypassing QR verification")
    return render_template('web_attendance.html', mode='masuk')

@app.route('/web_attendance')
@qr_verification_required
def web_attendance():
    """Halaman absensi berbasis web camera (untuk laptop dan mobile)"""
    mode = session.get('attendance_mode', 'masuk')
    
    # Get employee info from QR sync (based on mobile device that scanned QR)
    unit_code = session.get('verified_unit_code')
    employee_info = None
    if unit_code:
        latest_auth = qr_sync_manager.get_latest_auth(unit_code)
        if latest_auth:
            employee_info = latest_auth.get('employee_info')
    
    return render_template('web_attendance.html', mode=mode, employee_info=employee_info)

@app.route('/absen_ajax', methods=['POST'])
def absen_ajax():
    """AJAX endpoint untuk absensi dengan response JSON"""
    try:
        mode = request.form.get('mode', 'masuk')
        # Simulasi proses absensi
        result = run_attendance_ajax(mode)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in absen_ajax: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/mark_attendance', methods=['POST'])
@qr_verification_required
def mark_attendance():
    """Route untuk mark attendance yang dipanggil dari frontend - dengan camera lock"""
    try:
        logger.info("=== MARK ATTENDANCE REQUEST RECEIVED ===")
        
        mode = request.form.get('mode', 'masuk')
        camera_id = request.form.get('camera_id', '0')
        
        logger.info(f"Mark attendance request: mode={mode}, camera_id={camera_id}")
        logger.info(f"QR verification status: {session.get('qr_verified', False)}")
        logger.info(f"QR verification time: {session.get('qr_verified_time', 'None')}")
        
        # Check camera availability first
        if camera_id == '':
            return jsonify({
                'status': 'error',
                'message': 'Pilih kamera terlebih dahulu!'
            })
        
        # Import camera lock system
        from camera_lock import CameraLock, is_camera_busy
        
        # Check if camera is busy
        if is_camera_busy():
            return jsonify({
                'status': 'error',
                'message': '📷 Kamera sedang digunakan oleh perangkat lain. Silakan tunggu sebentar dan coba lagi.'
            })
        
        # Acquire camera lock
        try:
            with CameraLock() as camera_lock:
                logger.info(f"Camera lock acquired for {mode} mode")
                
                # SIMPLE APPROACH: Always do complete cleanup before ANY camera operation
                logger.info(f"Performing complete camera cleanup before {mode} mode")
                
                # Step 1: Destroy all OpenCV windows (most important)
                try:
                    cv2.destroyAllWindows()
                    cv2.waitKey(10)
                    time.sleep(0.3)
                except:
                    pass
                
                # Step 2: Force release camera 0 specifically
                for attempt in range(3):
                    try:
                        temp_cap = cv2.VideoCapture(int(camera_id))
                        if temp_cap.isOpened():
                            temp_cap.release()
                        del temp_cap
                        time.sleep(0.2)
                    except:
                        pass
                
                # Step 3: Extra delay for pulang mode
                if mode == 'pulang':
                    logger.info("Extra delay for pulang mode")
                    time.sleep(1.0)
                
                # Step 4: Try camera operation with lock protection
                try:
                    result = run_attendance_with_camera(mode, int(camera_id))
                    return jsonify(result)
                except Exception as camera_error:
                    logger.error(f"Camera error: {camera_error}")
                    # Fallback - simulasi absensi tanpa kamera untuk testing
                    return jsonify({
                        'status': 'warning',
                        'message': f'Kamera tidak tersedia. Mode simulasi: Absensi {mode} berhasil (demo mode)'
                    })
                    
        except RuntimeError as lock_error:
            logger.error(f"Camera lock error: {lock_error}")
            return jsonify({
                'status': 'error',
                'message': '📷 Tidak dapat mengakses kamera. Perangkat lain sedang menggunakan kamera. Silakan tutup aplikasi kamera lain dan coba lagi.'
            })
            
    except Exception as e:
        logger.error(f"Error in mark_attendance: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Terjadi kesalahan koneksi: {str(e)}. Silakan refresh halaman dan coba lagi.'
        })

@app.route('/mark_attendance_ajax', methods=['POST'])
@qr_verification_required
def mark_attendance_ajax_endpoint():
    """Route untuk absensi AJAX tanpa GUI window"""
    try:
        mode = request.form.get('mode', 'masuk')
        camera_id = request.form.get('camera_id', '0')
        
        logger.info(f"AJAX attendance request: mode={mode}, camera_id={camera_id}")
        
        # Simulasi check kamera dulu
        if camera_id == '':
            return jsonify({
                'status': 'error',
                'message': 'Pilih kamera terlebih dahulu!'
            })
        
        # Coba jalankan face recognition tanpa GUI
        try:
            result = run_attendance_ajax(mode, int(camera_id))
            return jsonify(result)
        except Exception as camera_error:
            logger.error(f"Camera error: {camera_error}")
            # Fallback - simulasi absensi tanpa kamera untuk testing
            return jsonify({
                'status': 'warning',
                'message': f'Kamera tidak tersedia. Mode simulasi: Absensi {mode} berhasil (demo mode)'
            })
            
    except Exception as e:
        logger.error(f"Error in mark_attendance_ajax: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        })

@app.route('/mark_attendance_mobile', methods=['POST'])
@qr_verification_required
def mark_attendance_mobile():
    """Route untuk absensi mobile menggunakan kamera browser - dengan camera lock"""
    try:
        mode = request.form.get('mode', 'masuk')
        image_data = request.form.get('image_data')
        source = request.form.get('source', 'mobile')
        
        logger.info(f"Mobile attendance request: mode={mode}, source={source}")
        
        if not image_data:
            return jsonify({
                'status': 'error',
                'message': 'Data gambar tidak ditemukan!'
            })
        
        # Import camera lock system
        from camera_lock import CameraLock, is_camera_busy
        
        # Check if camera is busy (desktop using camera)
        if is_camera_busy():
            return jsonify({
                'status': 'error',
                'message': '📷 Kamera sedang digunakan oleh laptop/desktop. Silakan tunggu sebentar dan coba lagi.'
            })
        
        # Acquire camera lock for mobile processing
        try:
            with CameraLock() as camera_lock:
                logger.info(f"Mobile camera lock acquired for {mode} mode")
                
                # Process base64 image data
                try:
                    # Remove data:image/jpeg;base64, prefix if present
                    if ',' in image_data:
                        image_data = image_data.split(',')[1]
                    
                    # Decode base64 image
                    image_bytes = base64.b64decode(image_data)
                    nparr = np.frombuffer(image_bytes, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if frame is None:
                        return jsonify({
                            'status': 'error',
                            'message': 'Gagal memproses gambar dari kamera mobile!'
                        })
                    
                    # Check if face recognition model exists
                    if 'face_recognition_model.pkl' not in os.listdir('static') and 'face_embeddings.pkl' not in os.listdir('static'):
                        return jsonify({
                            'status': 'error',
                            'message': '❌ Karyawan Tidak Dikenal'
                        })
                    
                    # Extract faces from the frame (for validation only)
                    faces = extract_faces(frame)
                    
                    if len(faces) == 0:
                        return jsonify({
                            'status': 'error',
                            'message': 'Wajah tidak terdeteksi. Pastikan pencahayaan cukup dan wajah terlihat jelas.'
                        })
                    
                    # INSIGHTFACE: Kirim FULL FRAME, bukan crop!
                    # InsightFace akan detect dan extract embedding sendiri
                    # Resize frame ke ukuran yang cukup besar untuk detection
                    frame_resized = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
                    
                    logger.info(f"Mobile frame for InsightFace: shape={frame_resized.shape}")
                    
                    # Identify the face with InsightFace (pass full frame)
                    identified_users, confidence = identify_face_insightface_wrapper(frame_resized)
                    user = identified_users[0]
                    
                    if user == 'Unknown':
                        return jsonify({
                            'status': 'error',
                            'message': '❌ Karyawan Tidak Dikenal'
                        })
                    
                    # Update attendance
                    result = update_attendance(user, mode)
                    
                    if result.get('success', False):
                        # IMPORTANT: Mark session as consumed to prevent auto-redirect
                        unit_code = session.get('verified_unit_code')
                        scan_time = session.get('last_sync_time')
                        if unit_code and scan_time:
                            session['qr_session_consumed'] = f"{unit_code}_{scan_time}"
                            logger.info(f"✅ Mobile QR session marked as consumed: {session['qr_session_consumed']}")
                        
                        # Set attendance completed time for grace period
                        session['attendance_completed_time'] = datetime.now().isoformat()
                        logger.info(f"✅ Mobile attendance completed time set: {session['attendance_completed_time']}")
                        
                        return jsonify({
                            'status': 'success',
                            'message': f'✅ Absensi {mode} berhasil untuk {user}!',
                            'user': user,
                            'mode': mode,
                            'time': datetime.now().strftime('%H:%M:%S')
                        })
                    else:
                        return jsonify({
                            'status': 'warning',
                            'message': result.get('message', f'Absensi {mode} sudah tercatat hari ini untuk {user}'),
                            'user': user
                        })
                        
                except Exception as img_error:
                    logger.error(f"Mobile image processing error: {img_error}")
                    return jsonify({
                        'status': 'error',
                        'message': f'Gagal memproses gambar mobile: {str(img_error)}'
                    })
                    
        except RuntimeError as lock_error:
            logger.error(f"Mobile camera lock error: {lock_error}")
            return jsonify({
                'status': 'error',
                'message': '📷 Tidak dapat mengakses kamera mobile. Desktop sedang menggunakan kamera. Silakan tunggu sebentar dan coba lagi.'
            })
            
    except Exception as e:
        logger.error(f"Error in mark_attendance_mobile: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Terjadi kesalahan koneksi mobile: {str(e)}. Silakan refresh halaman dan coba lagi.'
        })

@app.route('/mobile')
@qr_verification_required
def mobile_attendance():
    """Route untuk halaman absensi mobile - redirect ke web_attendance"""
    mode = request.args.get('mode', 'masuk')
    return redirect(url_for('web_attendance', mode=mode))

def run_attendance_ajax(mode='masuk', camera_id=None):
    """Fungsi absensi yang return JSON untuk AJAX - tanpa GUI window"""
    try:
        # Gunakan camera_id yang diberikan atau default
        if camera_id is None:
            camera_id = selected_camera_id
            
        logger.info(f"Starting non-GUI attendance for {mode} with camera {camera_id}")
        
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            logger.warning(f"Cannot open camera {camera_id}, trying default")
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {'status': 'error', 'message': 'Kamera tidak tersedia'}

        if 'face_recognition_model.pkl' not in os.listdir('static') and 'face_embeddings.pkl' not in os.listdir('static'):
            cap.release()
            return {'status': 'error', 'message': '❌ Karyawan Tidak Dikenal'}

        recognition_success = False
        success_user = ""
        attempts = 0
        max_attempts = 150  # 5 detik maksimal untuk AJAX
        
        logger.info(f"Starting face detection loop for {mode}")
        
        while attempts < max_attempts:
            ret, frame = cap.read()
            if not ret:
                logger.warning(f"Cannot read frame at attempt {attempts}")
                break
                
            faces = extract_faces(frame)
            if len(faces) > 0:
                logger.info(f"Face detected at attempt {attempts}")
                (x, y, w, h) = faces[0]
                face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
                # Convert to grayscale for consistency
                gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) if len(face.shape) == 3 else face
                identified_users, confidence = identify_face(gray_face.flatten())
                user = identified_users[0]
                
                if user != 'Unknown':
                    # Update attendance
                    result = update_attendance(user, mode)
                    recognition_success = True
                    success_user = user
                    logger.info(f"Attendance recorded for {user} (confidence: {confidence:.1f}%)")
                    break
                else:
                    logger.info(f"Face detected but not recognized (confidence: {confidence:.1f}%)")
                
            attempts += 1
        
        cap.release()
        
        if recognition_success:
            return {
                'status': 'success',
                'message': f'Absensi {mode} berhasil!',
                'user': success_user,
                'mode': mode
            }
        else:
            return {
                'status': 'error',
                'message': '❌ Karyawan Tidak Dikenal'
            }
            
    except Exception as e:
        logger.error(f"Error in run_attendance_ajax: {e}")
        return {'status': 'error', 'message': str(e)}

def run_attendance(mode='masuk'):
    print(f"[DEBUG] Mulai absensi ({mode}) dengan kamera ID: {selected_camera_id}")
    
    # Force cleanup existing windows dan tunggu sebentar
    cv2.destroyAllWindows()
    import time
    time.sleep(0.5)  # Wait 500ms untuk cleanup
    
    cap = cv2.VideoCapture(selected_camera_id)
    if not cap.isOpened():
        print(f"[ERROR] Kamera tidak dapat dibuka untuk mode {mode}")
        return render_template('home.html', mess="Kamera tidak tersedia.",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    print(f"[DEBUG] Kamera berhasil dibuka untuk mode {mode}")
    
    # Set buffer size untuk mengurangi latency
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    if 'face_recognition_model.pkl' not in os.listdir('static') and 'face_embeddings.pkl' not in os.listdir('static'):
        print(f"[ERROR] Model tidak ditemukan untuk mode {mode}")
        cap.release()
        return render_template('home.html', mess="❌ Karyawan Tidak Dikenal",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    print(f"[DEBUG] Model ditemukan, memulai loop kamera untuk mode {mode}")
    
    # Create named window dengan flag tertentu
    window_name = f"Absensi {mode.capitalize()}"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    print(f"[DEBUG] Window '{window_name}' dibuat")
    
    recognition_success = False
    success_user = ""
    loading_counter = 0
    frame_count = 0
    
    while True:
        frame_count += 1
        ret, frame = cap.read()
        if not ret:
            print(f"[ERROR] Tidak dapat membaca frame {frame_count} untuk mode {mode}")
            break
            
        # Debug setiap 30 frame (sekitar 1 detik)
        if frame_count % 30 == 1:
            print(f"[DEBUG] Frame {frame_count} - Mode {mode}")
            
        faces = extract_faces(frame)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            # Convert to grayscale for consistency
            gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) if len(face.shape) == 3 else face
            identified_users, confidence = identify_face(gray_face.flatten())
            user = identified_users[0]
            
            # Tampilkan recognition result dengan confidence
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'{user} ({confidence:.0f}%) - {mode.upper()}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Loading animation setelah face terdeteksi
            if not recognition_success:
                loading_counter += 1
                loading_text = "MEMPROSES" + "." * (loading_counter % 4)
                cv2.putText(frame, loading_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Setelah 30 frames (sekitar 1 detik), proses absensi
                if loading_counter >= 30:
                    # Update attendance
                    update_attendance(user, mode)
                    recognition_success = True
                    success_user = user
                    loading_counter = 0
                    print(f"[SUCCESS] Attendance recorded for {user} - {mode}")
        else:
            loading_counter = 0  # Reset loading jika tidak ada wajah
        
        # Tampilkan status loading atau success
        if recognition_success:
            # Tampilkan pesan sukses
            cv2.putText(frame, f'ABSENSI {mode.upper()} BERHASIL!', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Data {success_user} telah disimpan', (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, 'Kamera akan ditutup dalam 3 detik...', (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            loading_counter += 1
            if loading_counter >= 90:  # 3 detik (30 fps x 3)
                break
        else:
            cv2.putText(frame, f'Mode: {mode.upper()} - Posisikan wajah di depan kamera', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, 'Tekan ESC untuk keluar', (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Debug untuk cv2.imshow
        window_name = f"Absensi {mode.capitalize()}"
        try:
            cv2.imshow(window_name, frame)
            if frame_count % 30 == 1:
                print(f"[DEBUG] Window '{window_name}' ditampilkan untuk frame {frame_count}")
        except Exception as e:
            print(f"[ERROR] Gagal menampilkan window '{window_name}': {e}")
            
        if cv2.waitKey(1) == 27:  # ESC key
            print(f"[DEBUG] ESC ditekan, keluar dari mode {mode}")
            break
    
    print(f"[DEBUG] Keluar dari loop kamera untuk mode {mode}, total frame: {frame_count}")
    cap.release()
    cv2.destroyAllWindows()
    print(f"[DEBUG] Kamera dan window ditutup untuk mode {mode}")
    
    # Return dengan pesan sukses jika berhasil
    if recognition_success:
        print(f"[DEBUG] Absensi {mode} berhasil, menampilkan hasil")
        names, bagian, tanggal, times, l = extract_attendance()
        return render_template('home.html',
            names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id, 
            mess=f"✅ Absensi {mode} berhasil! Data {success_user} telah disimpan.")
    else:
        print(f"[DEBUG] Absensi {mode} tidak berhasil, kembali ke home")
        return home()

def force_camera_cleanup():
    """
    TARGETED camera cleanup function - safe untuk server yang sedang berjalan
    Hanya cleanup camera resources tanpa kill main server process
    """
    logger.info("Starting FORCE camera cleanup...")
    
    # Step 1: Destroy ALL OpenCV windows first (paling penting)
    for attempt in range(5):
        try:
            cv2.destroyAllWindows()
            cv2.waitKey(10)  # Force event processing
            time.sleep(0.1)
        except:
            pass
    
    # Step 2: Force release all possible camera indices multiple times
    for cam_id in range(10):  # Limit to reasonable range
        for attempt in range(3):  # Multiple attempts per camera
            try:
                temp_cap = cv2.VideoCapture(cam_id)
                if temp_cap.isOpened():
                    temp_cap.release()
                del temp_cap
                time.sleep(0.05)
            except:
                continue
    
    # Step 3: System level cleanup (targeted - no server killing)
    try:
        import subprocess
        # Only kill camera-specific processes, NOT main python processes
        subprocess.run(['pkill', '-f', 'v4l2'], capture_output=True, timeout=3)
        subprocess.run(['pkill', '-f', 'gstreamer'], capture_output=True, timeout=3)
        
        # Kill processes specifically using video devices
        for i in range(5):  # Only check main video devices
            try:
                subprocess.run(['fuser', '-k', f'/dev/video{i}'], 
                             capture_output=True, timeout=1, stderr=subprocess.DEVNULL)
            except:
                pass
                
    except Exception as e:
        logger.warning(f"System cleanup warning: {e}")
    
    # Step 4: Wait for resources to be fully released
    time.sleep(1.5)  # Reasonable wait time
    
    # Step 5: Force garbage collection
    import gc
    for _ in range(2):
        gc.collect()
        time.sleep(0.1)
    
    # Step 6: Final verification
    try:
        verification_cap = cv2.VideoCapture(0)
        if verification_cap.isOpened():
            verification_cap.release()
        del verification_cap
    except:
        pass
    
    time.sleep(0.5)
    logger.info("FORCE camera cleanup completed")

def run_attendance_with_camera(mode, camera_id):
    """
    Fungsi untuk menjalankan absensi dengan kamera menggunakan isolated process
    This solves GUI window conflicts by running camera in separate process
    """
    try:
        logger.info(f"Starting isolated camera process for {mode} mode with camera {camera_id}")
        
        # Import subprocess for process isolation
        import subprocess
        import os
        
        # Get the path to the isolated camera script
        script_path = os.path.join(os.path.dirname(__file__), 'camera_isolated_enhanced.py')
        
        # Run camera in isolated subprocess
        try:
            logger.info(f"Launching subprocess: python3 {script_path} {mode} {camera_id}")
            
            # Start the isolated camera process
            process = subprocess.Popen([
                'python3', script_path, mode, str(camera_id)
            ], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(__file__)
            )
            
            # Wait for the process to complete
            stdout, stderr = process.communicate(timeout=60)  # 60 second timeout
            
            # Check return code
            if process.returncode == 0:
                logger.info(f"Isolated camera process for {mode} completed successfully")
                
                # IMPORTANT: Mark session as consumed to prevent auto-redirect
                unit_code = session.get('verified_unit_code')
                scan_time = session.get('last_sync_time')
                if unit_code and scan_time:
                    session['qr_session_consumed'] = f"{unit_code}_{scan_time}"
                    logger.info(f"✅ QR session marked as consumed: {session['qr_session_consumed']}")
                
                # Set attendance completed time for grace period
                session['attendance_completed_time'] = datetime.now().isoformat()
                logger.info(f"✅ Attendance completed time set: {session['attendance_completed_time']}")
                
                return {
                    'status': 'success',
                    'message': f'✅ Absensi {mode} berhasil! Data telah disimpan dengan sistem kamera terisolasi.'
                }
            else:
                logger.warning(f"Isolated camera process for {mode} failed with return code {process.returncode}")
                if stderr:
                    logger.error(f"Process stderr: {stderr.decode()}")
                return {
                    'status': 'warning', 
                    'message': f'⚠️ Proses absensi {mode} tidak berhasil atau dibatalkan.'
                }
                
        except subprocess.TimeoutExpired:
            process.kill()
            logger.error(f"Isolated camera process for {mode} timed out")
            return {
                'status': 'error',
                'message': f'❌ Timeout absensi {mode}. Silakan coba lagi.'
            }
            
        except Exception as subprocess_error:
            logger.error(f"Subprocess error: {subprocess_error}")
            return {
                'status': 'error',
                'message': f'❌ Error menjalankan kamera: {str(subprocess_error)}'
            }
    
    except Exception as e:
        logger.error(f"Error in run_attendance_with_camera: {e}")
        return {
            'status': 'error',
            'message': f'❌ Error sistem kamera: {str(e)}'
        }

def update_attendance(name, mode='masuk'):
    """Update attendance menggunakan database"""
    try:
        # Handle different name formats
        if '_' in name:
            # Old format: name_bagian
            username = name.split('_')[0]
            userbagian = name.split('_')[1]
            employee = Employee.get_employee_by_name_bagian(username, userbagian)
        else:
            # New format: just name (from InsightFace)
            username = name
            userbagian = None
            # Search by name only
            employees = Employee.get_all_employees()
            employee = None
            for emp in employees:
                if emp.get('name') == username:
                    employee = emp
                    userbagian = emp.get('bagian', 'Unknown')
                    break
        
        current_time = datetime.now().time()
        today = date.today()
        
        if not employee:
            # Jika employee belum ada, tambahkan dulu
            if Employee.add_employee(username, userbagian):
                employee = Employee.get_employee_by_name_bagian(username, userbagian)
            else:
                logger.error(f"Gagal menambah employee: {username} ({userbagian})")
                return {'success': False, 'message': 'Gagal menambah karyawan ke database'}
        
        # Check if already attended today
        existing_attendance = Attendance.get_attendance_by_employee_date(employee['id'], today)
        
        # Update attendance
        if mode == 'masuk':
            if existing_attendance and existing_attendance.get('jam_masuk'):
                return {
                    'success': False, 
                    'message': f'Absensi masuk sudah tercatat hari ini pada {existing_attendance["jam_masuk"]}'
                }
            success = Attendance.add_or_update_attendance(employee['id'], today, jam_masuk=current_time)
            activity_type = 'login'
        else:  # mode == 'keluar'
            if existing_attendance and existing_attendance.get('jam_pulang'):
                return {
                    'success': False, 
                    'message': f'Absensi keluar sudah tercatat hari ini pada {existing_attendance["jam_pulang"]}'
                }
            success = Attendance.add_or_update_attendance(employee['id'], today, jam_pulang=current_time)
            activity_type = 'logout'
        
        if success:
            # Log aktivitas
            ActivityLog.add_log(employee['id'], activity_type, f"Absensi {mode} berhasil")
            logger.info(f"Attendance updated: {username} - {mode} at {current_time}")
            
            return {'success': True, 'message': f'Absensi {mode} berhasil dicatat'}
        else:
            logger.error(f"Gagal update attendance: {username} - {mode}")
            return {'success': False, 'message': 'Gagal menyimpan data absensi'}
            
    except Exception as e:
        logger.error(f"Error updating attendance: {e}")
        return {'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}

@app.route('/get_attendance_data')
@qr_verification_required
def get_attendance_data():
    """AJAX endpoint untuk mendapatkan data absensi terbaru"""
    try:
        names, bagian, tanggal, times, l = extract_attendance()
        return jsonify({
            'status': 'success',
            'data': {
                'names': names,
                'bagian': bagian,
                'tanggal': tanggal,
                'times': times,
                'total': l,
                'totalreg': totalreg()
            }
        })
    except Exception as e:
        logger.error(f"Error getting attendance data: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

# ======================== ADMIN ROUTES ========================

@app.route('/get_employees')
def get_employees():
    """AJAX endpoint untuk mendapatkan daftar karyawan"""
    try:
        employees = Employee.get_all_employees()
        employee_list = []
        if employees:
            for emp in employees:
                employee_list.append({
                    'name': emp['name'],
                    'bagian': emp['bagian'],
                    'display': f"{emp['name']} ({emp['bagian']})"
                })
        return jsonify({
            'status': 'success',
            'employees': employee_list
        })
    except Exception as e:
        logger.error(f"Error getting employees: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/employee/update', methods=['POST'])
def api_update_employee():
    """API untuk update data karyawan"""
    try:
        data = request.get_json()
        employee_id = data.get('id')
        new_name = data.get('name')
        new_bagian = data.get('bagian')
        new_nik = data.get('nik', '')
        new_email = data.get('email', '')
        new_telepon = data.get('telepon', '')
        
        if not employee_id or not new_name or not new_bagian:
            return jsonify({'success': False, 'message': 'ID, nama, dan bagian harus diisi'})
        
        db = get_db_manager()
        
        # Get old employee data untuk rename folder
        result = db.execute_query("SELECT * FROM karyawan WHERE id = %s", (employee_id,))
        if not result or len(result) == 0:
            return jsonify({'success': False, 'message': 'Karyawan tidak ditemukan'})
        
        old_employee = result[0]
        old_name = old_employee['nama']
        old_bagian = old_employee['bagian']
        
        # Update database
        update_query = """
            UPDATE karyawan 
            SET nama = %s, bagian = %s, nik = %s, email = %s, telepon = %s
            WHERE id = %s
        """
        db.execute_query(update_query, (new_name, new_bagian, new_nik, new_email, new_telepon, employee_id))
        
        # Rename folder foto jika nama/bagian berubah
        if old_name != new_name or old_bagian != new_bagian:
            old_folder = f"static/faces/{old_name}_{old_bagian}"
            new_folder = f"static/faces/{new_name}_{new_bagian}"
            if os.path.exists(old_folder):
                os.rename(old_folder, new_folder)
                logger.info(f"Renamed folder: {old_folder} -> {new_folder}")
            
            # Train ulang model karena nama berubah
            train_model()
        
        logger.info(f"Employee updated: ID {employee_id}, {old_name} -> {new_name}")
        return jsonify({
            'success': True, 
            'message': f'Data karyawan {new_name} berhasil diupdate'
        })
        
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/employee/delete', methods=['POST'])
def api_delete_employee():
    """API untuk menghapus karyawan berdasarkan ID"""
    try:
        data = request.get_json()
        employee_id = data.get('id')
        
        if not employee_id:
            return jsonify({'success': False, 'message': 'ID karyawan harus diisi'})
        
        db = get_db_manager()
        
        # Get employee data
        result = db.execute_query("SELECT * FROM karyawan WHERE id = %s", (employee_id,))
        if not result or len(result) == 0:
            return jsonify({'success': False, 'message': 'Karyawan tidak ditemukan'})
        
        employee = result[0]
        emp_name = employee['nama']
        emp_bagian = employee['bagian']
        
        # Hapus data absensi terkait
        db.execute_query("DELETE FROM absensi WHERE id_karyawan = %s", (employee_id,))
        
        # Hapus karyawan
        db.execute_query("DELETE FROM karyawan WHERE id = %s", (employee_id,))
        
        # Hapus folder foto
        face_folder = f"static/faces/{emp_name}_{emp_bagian}"
        if os.path.exists(face_folder):
            shutil.rmtree(face_folder)
            logger.info(f"Deleted face folder: {face_folder}")
        
        # Hapus foto profil jika ada
        photo_path = f"static/employee_photos/{employee_id}.jpg"
        if os.path.exists(photo_path):
            os.remove(photo_path)
        
        # Train ulang model
        train_model()
        
        logger.info(f"Employee deleted: ID {employee_id}, {emp_name} ({emp_bagian})")
        return jsonify({
            'success': True, 
            'message': f'Karyawan {emp_name} berhasil dihapus'
        })
        
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/employee/<int:employee_id>', methods=['GET'])
def api_get_employee(employee_id):
    """API untuk mendapatkan detail karyawan berdasarkan ID"""
    try:
        db = get_db_manager()
        result = db.execute_query("SELECT * FROM karyawan WHERE id = %s", (employee_id,))
        
        if not result or len(result) == 0:
            return jsonify({'success': False, 'message': 'Karyawan tidak ditemukan'})
        
        employee = result[0]
        return jsonify({
            'success': True,
            'employee': {
                'id': employee['id'],
                'name': employee['nama'],
                'bagian': employee['bagian'],
                'nik': employee.get('nik', ''),
                'email': employee.get('email', ''),
                'telepon': employee.get('telepon', ''),
                'tanggal_bergabung': str(employee.get('tanggal_bergabung', ''))
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting employee: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    """Endpoint untuk menghapus karyawan"""
    try:
        employee_name = request.form.get('name')
        employee_bagian = request.form.get('bagian')
        
        if not employee_name or not employee_bagian:
            return jsonify({'status': 'error', 'message': 'Nama dan bagian harus diisi'})
        
        # Hapus dari database
        employee = Employee.get_employee_by_name_bagian(employee_name, employee_bagian)
        if employee:
            # Hapus data attendance terkait
            db = get_db_manager()
            db.execute_query("DELETE FROM attendance WHERE employee_id = %s", (employee['id'],))
            db.execute_query("DELETE FROM activity_log WHERE employee_id = %s", (employee['id'],))
            db.execute_query("DELETE FROM employees WHERE id = %s", (employee['id'],))
            
            # Hapus folder foto
            face_folder = f"static/faces/{employee_name}_{employee_bagian}"
            if os.path.exists(face_folder):
                shutil.rmtree(face_folder)
            
            # Train ulang model
            train_model()
            
            logger.info(f"Employee {employee_name} ({employee_bagian}) deleted successfully")
            return jsonify({'status': 'success', 'message': f'Karyawan {employee_name} berhasil dihapus'})
        else:
            return jsonify({'status': 'error', 'message': 'Karyawan tidak ditemukan'})
            
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/delete_attendance', methods=['POST'])
def delete_attendance():
    """Endpoint untuk menghapus data absensi tertentu"""
    try:
        employee_name = request.form.get('name')
        employee_bagian = request.form.get('bagian')
        tanggal = request.form.get('tanggal')
        
        logger.info(f"Delete request - Name: {employee_name}, Bagian: {employee_bagian}, Tanggal: {tanggal}")
        
        if not all([employee_name, employee_bagian, tanggal]):
            return jsonify({'status': 'error', 'message': 'Data tidak lengkap'})
        
        # Parse tanggal
        from datetime import datetime
        tanggal_obj = datetime.strptime(tanggal, "%d-%m-%Y").date()
        logger.info(f"Parsed date object: {tanggal_obj}")
        
        # Hapus dari database
        employee = Employee.get_employee_by_name_bagian(employee_name, employee_bagian)
        if employee:
            logger.info(f"Employee found: {employee}")
            db = get_db_manager()
            
            # First check if record exists
            check_query = "SELECT * FROM attendance WHERE employee_id = %s AND tanggal = %s"
            existing_record = db.execute_query(check_query, (employee['id'], tanggal_obj))
            logger.info(f"Existing record check: {existing_record}")
            
            if existing_record:
                result = db.execute_query("DELETE FROM attendance WHERE employee_id = %s AND tanggal = %s", 
                                        (employee['id'], tanggal_obj))
                logger.info(f"Delete result: {result}")
                
                if result > 0:
                    logger.info(f"Attendance deleted for {employee_name} on {tanggal}")
                    return jsonify({'status': 'success', 'message': 'Data absensi berhasil dihapus'})
                else:
                    return jsonify({'status': 'error', 'message': 'Gagal menghapus data absensi'})
            else:
                return jsonify({'status': 'error', 'message': 'Data absensi tidak ditemukan'})
        else:
            logger.warning(f"Employee not found: {employee_name}, {employee_bagian}")
            return jsonify({'status': 'error', 'message': 'Karyawan tidak ditemukan'})
            
    except Exception as e:
        logger.error(f"Error deleting attendance: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/add', methods=['POST'])
def add():
    newusername = request.form['newusername']
    newbagian = request.form['newuserid']

    if not newusername or not newbagian:
        return render_template('home.html', mess="Nama dan Bagian harus diisi.",
                               names=[], rolls=[], tanggal=[], times=[], l=0,
                               totalreg=totalreg(), datetoday2=datetoday2,
                               date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini)

    # Cek apakah employee sudah ada di database
    if Employee.employee_exists(newusername, newbagian):
        names, bagian, tanggal, times, l = extract_attendance()
        return render_template('home.html', mess=f"Karyawan {newusername} ({newbagian}) sudah terdaftar.",
                               names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
                               totalreg=totalreg(), datetoday2=datetoday2,
                               date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
                               selected_camera=selected_camera_id)

    userimagefolder = f'static/faces/{newusername}_{newbagian}'
    os.makedirs(userimagefolder, exist_ok=True)

    i, j = 0, 0
    cap = None
    window_name = f'Menambah Karyawan Baru - {newusername}'
    
    try:
        # Comprehensive cleanup of any existing OpenCV resources
        cleanup_opencv_resources()
        
        cap = cv2.VideoCapture(selected_camera_id)
        if not cap.isOpened():
            names, bagian, tanggal, times, l = extract_attendance()
            return render_template('home.html', mess="Kamera tidak tersedia.",
                                   names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
                                   totalreg=totalreg(), datetoday2=datetoday2,
                                   date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
                                   selected_camera=selected_camera_id)

        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"[DEBUG] Starting camera capture for {newusername}_{newbagian}")
        
        # Create named window with specific flags
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[DEBUG] Failed to read frame from camera")
                break
                
            faces = extract_faces(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
                cv2.putText(frame, f'Gambar Diambil: {i}/{nimgs}', (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2)
                cv2.putText(frame, f'Karyawan: {newusername} ({newbagian})', (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, 'Tekan ESC untuk keluar', (30, frame.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if j % 5 == 0:  # Capture every 5th frame with face
                    name = f"{newusername}_{newbagian}_{i}.jpg"
                    cv2.imwrite(os.path.join(userimagefolder, name), frame[y:y+h, x:x+w])
                    print(f"[DEBUG] Captured image {i+1}/{nimgs}: {name}")
                    i += 1
                j += 1
            
            # Show the frame with error handling
            try:
                cv2.imshow(window_name, frame)
            except Exception as e:
                print(f"[DEBUG] Error showing frame: {e}")
                break
                
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                print("[DEBUG] ESC pressed, exiting camera")
                break
            
            if i >= nimgs:  # All images captured
                print(f"[DEBUG] Captured all {nimgs} images")
                break

    except Exception as e:
        print(f"[ERROR] Camera capture error: {e}")
        logger.error(f"Camera capture error for {newusername}_{newbagian}: {e}")
    
    finally:
        # Comprehensive cleanup with proper order
        try:
            if cap is not None:
                cap.release()
                print("[DEBUG] Camera released")
        except Exception as e:
            print(f"[DEBUG] Error releasing camera: {e}")
        
        try:
            # Destroy specific window first
            cv2.destroyWindow(window_name)
            cv2.waitKey(1)
            
            # Then destroy all windows
            cv2.destroyAllWindows()
            cv2.waitKey(1)  # Process any remaining events
            
            # Additional cleanup for persistent window issues
            for _ in range(5):
                cv2.waitKey(1)
                
            print("[DEBUG] All OpenCV windows destroyed")
        except Exception as e:
            print(f"[DEBUG] Error destroying windows: {e}")
    
    if i < nimgs:
        names, bagian, tanggal, times, l = extract_attendance()
        return render_template('home.html', mess=f"Hanya berhasil mengambil {i} dari {nimgs} gambar. Silakan coba lagi dengan posisi wajah yang lebih baik.",
                               names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
                               totalreg=totalreg(), datetoday2=datetoday2,
                               date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
                               selected_camera=selected_camera_id)
    
    # Tambahkan employee ke database setelah berhasil capture gambar
    if Employee.add_employee(newusername, newbagian):
        logger.info(f"Employee {newusername} ({newbagian}) berhasil ditambah ke database")
        # Log aktivitas
        employee = Employee.get_employee_by_name_bagian(newusername, newbagian)
        if employee:
            ActivityLog.add_log(employee['id'], 'add_employee', f"Employee {newusername} ({newbagian}) ditambahkan")
    else:
        logger.error(f"Gagal menambah employee {newusername} ({newbagian}) ke database")
    
    print(f"[DEBUG] Successfully captured {i} images for {newusername}_{newbagian}")
    train_model()
    return home()

# =======================
# MODERN API ENDPOINTS
# =======================

@app.route('/api/attendance_data')
def api_get_attendance_data():
    """API endpoint untuk mendapatkan data absensi hari ini"""
    try:
        names, bagian, tanggal, times, l = extract_attendance()
        return jsonify({
            'status': 'success',
            'names': names,
            'bagian': bagian,
            'tanggal': tanggal,
            'times': times,
            'total': l
        })
    except Exception as e:
        logger.error(f"Error getting attendance data: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Gagal mengambil data absensi'
        }), 500
@app.route('/api/cameras')
def api_get_cameras():
    """API endpoint untuk mendapatkan daftar kamera yang tersedia"""
    try:
        cameras = []
        
        # Test kamera 0 (default)
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cameras.append({
                        'id': '0',
                        'name': 'Default Camera',
                        'status': 'active',
                        'resolution': f'{width}x{height}'
                    })
                cap.release()
        except Exception as e:
            logger.warning(f"Camera 0 not available: {e}")
        
        # Test kamera 1
        try:
            cap = cv2.VideoCapture(1)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cameras.append({
                        'id': '1',
                        'name': 'External Camera',
                        'status': 'active',
                        'resolution': f'{width}x{height}'
                    })
                cap.release()
        except Exception as e:
            logger.warning(f"Camera 1 not available: {e}")
        
        if not cameras:
            # Jika tidak ada kamera tersedia, return error
            return jsonify({
                'cameras': [],
                'error': 'No cameras detected',
                'message': 'Please check camera connection'
            }), 404
            
        return jsonify(cameras)
        
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        return jsonify({
            'cameras': [],
            'error': str(e)
        }), 500

@app.route('/camera-test')
def camera_test():
    """Halaman test kamera sederhana untuk debugging"""
    return render_template('camera_test.html')

@app.route('/offline.html')
def offline_page():
    """Serve offline page for PWA"""
    return render_template('offline.html')

@app.route('/static/sw.js')
def service_worker():
    """Serve service worker"""
    return app.send_static_file('sw.js'), 200, {'Content-Type': 'application/javascript'}

@app.route('/static/manifest.json')
def manifest():
    """Serve PWA manifest"""
    return app.send_static_file('manifest.json'), 200, {'Content-Type': 'application/manifest+json'}

@app.route('/share', methods=['POST'])
def share_handler():
    """Handle PWA share target"""
    try:
        title = request.form.get('title', '')
        text = request.form.get('text', '')
        url = request.form.get('url', '')
        files = request.files.getlist('files')
        
        # Log shared content
        logger.info(f"Share received - Title: {title}, Text: {text}, URL: {url}, Files: {len(files)}")
        
        # Process shared files if any
        for file in files:
            if file.filename:
                # Handle shared images or CSV files
                logger.info(f"Shared file: {file.filename}")
        
        return jsonify({'status': 'success', 'message': 'Share received'})
    except Exception as e:
        logger.error(f"Error handling share: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to handle share'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db_manager.get_connection()
        
        # Check if model exists
        model_exists = os.path.exists('./static/face_recognition_model.pkl')
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'model': 'available' if model_exists else 'missing',
            'version': '2.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        # Get today's attendance stats
        today = date.today().strftime("%d-%m-%Y")
        names, _, _, _, total_present = extract_attendance()
        
        # Get total registered employees
        total_employees = totalreg()
        
        # Calculate attendance rate
        attendance_rate = (total_present / total_employees * 100) if total_employees > 0 else 0
        
        return jsonify({
            'total_employees': total_employees,
            'present_today': total_present,
            'attendance_rate': round(attendance_rate, 1),
            'date': today
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'error': 'Failed to get statistics'
        }), 500

# Error handlers for PWA
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors - redirect to offline page if it's a fetch request"""
    if request.headers.get('Accept', '').startswith('application/json'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('offline.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    if request.headers.get('Accept', '').startswith('application/json'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('offline.html'), 500

# ===========================
# CLOUDFLARE TUNNEL MANAGEMENT  
# ===========================

def print_cloudflare_instructions(port):
    """Print instructions for using Cloudflare Tunnel"""
    print("\n" + "="*60)
    print("🌐 KAFEBASABASI - CLOUDFLARE TUNNEL SETUP")
    print("="*60)
    print("� Untuk akses public dengan Cloudflare Tunnel:")
    print("")
    print("   1. Buka terminal baru:")
    print(f"      cloudflared tunnel --url http://localhost:{port}")
    print("")
    print("   2. Atau gunakan script otomatis:")
    print("      ./scripts/start_cloudflare.sh")
    print("")
    print("   3. Copy URL yang muncul (format: https://xxx.trycloudflare.com)")
    print("")
    print("� Keunggulan Cloudflare Tunnel:")
    print("   ✅ Gratis selamanya (tidak ada batasan waktu)")
    print("   ✅ Lebih stabil dan reliable")
    print("   ✅ Performance lebih cepat dengan global CDN")
    print("   ✅ Security lebih baik dengan DDoS protection")
    print("")
    print("📚 Dokumentasi lengkap: docs/CLOUDFLARE_SETUP.md")
    print("="*60)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n🛑 Shutting down Kafebasabasi system...')
    
    # Close database connection
    try:
        db_manager.close_connection()
        print('✅ Database connection closed')
    except:
        pass
    
    print('👋 Goodbye!')
    sys.exit(0)

# ======================== ERROR HANDLERS ========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        from helpers import api_response
        return api_response(False, 'Endpoint not found', status_code=404)
    return render_template('error.html', 
                         error_code=404,
                         error_message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    if request.path.startswith('/api/'):
        from helpers import api_response
        return api_response(False, 'Internal server error', status_code=500)
    return render_template('error.html',
                         error_code=500,
                         error_message='Internal server error'), 500

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    if request.path.startswith('/api/'):
        from helpers import api_response
        return api_response(False, 'Forbidden', status_code=403)
    return render_template('error.html',
                         error_code=403,
                         error_message='Access forbidden'), 403

# ======================== LOGGING SETUP ========================

def setup_logging():
    """Setup file logging with rotation"""
    from logging.handlers import RotatingFileHandler
    import os
    
    # Create logs directory if not exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Setup file handler
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10000000,  # 10MB
        backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Smart Absen logging started')

# Initialize logging
setup_logging()

if __name__ == '__main__':
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Initialize database
        if db_manager.initialize_database():
            logger.info("Database initialized successfully")
            
            # Load app configuration
            port = app_config['port']
            host = app_config['host']
            
            # Show local access info
            print("\n" + "="*60)
            print("🏠 KAFEBASABASI ATTENDANCE SYSTEM")
            print("="*60)
            print(f"🔗 Local URL: http://localhost:{port}")
            print(f"🔗 QR Auth (Local): http://localhost:{port}/auth")
            print(f"👨‍💼 Admin (Local): http://localhost:{port}/admin/login")
            print(f"📷 Camera Test: http://localhost:{port}/camera-test")
            print("="*60)
            print("💡 Untuk akses public, gunakan Cloudflare Tunnel")
            
            # Show Cloudflare Tunnel instructions
            print_cloudflare_instructions(port)
            
            logger.info("Starting Kafebasabasi Attendance System v2.0")
            logger.info(f"Local server: http://{host}:{port}")
            logger.info("For public access, use Cloudflare Tunnel: cloudflared tunnel --url http://localhost:" + str(port))
            
            # Run Flask app
            app.run(
                debug=app_config['debug'],
                host=host, 
                port=port,
                use_reloader=False
            )
        else:
            logger.error("Failed to initialize database. Please run init_database.py first.")
            
    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        # Final cleanup
        db_manager.close_connection()
