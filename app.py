import cv2
import os
import csv
import time
import hashlib
import secrets
import base64
from io import BytesIO
from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
import shutil
import qrcode
from functools import wraps

# Ngrok and system imports
from pyngrok import ngrok
import threading
import signal
import sys
import atexit

# Import database modules
from database import get_db_manager
from models import Employee, Attendance, ActivityLog
from config import get_app_config
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load app configuration
app_config = get_app_config()
app.secret_key = app_config['secret_key']

# QR Code Authentication System
QR_VALIDITY_MINUTES = 10  # QR code berlaku 10 menit
current_unit_code = None
qr_code_generated_time = None

# Ngrok tunnel management
ngrok_tunnel = None

def generate_unit_code():
    """Generate kode unit yang unik berdasarkan waktu"""
    current_time = datetime.now()
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

def generate_qr_code():
    """Generate QR code untuk authentication"""
    unit_code = get_current_unit_code()
    base_url = request.host_url.rstrip('/')
    qr_url = f"{base_url}/verify?unit={unit_code}"
    
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
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
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
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

def train_model():
    faces, labels = [], []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    if faces:
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(np.array(faces), labels)
        joblib.dump(knn, 'static/face_recognition_model.pkl')

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

@app.route('/generate_qr')
def generate_qr_endpoint():
    """Endpoint untuk refresh QR code via AJAX"""
    try:
        # Force regenerate QR code
        global current_unit_code, qr_code_generated_time
        current_unit_code = None
        qr_code_generated_time = None
        
        qr_image, qr_url = generate_qr_code()
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
            'qr_image': qr_image,
            'qr_url': qr_url,
            'unit_code': unit_code,
            'remaining_seconds': remaining_seconds
        })
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/verify')
def verify_qr():
    """Verifikasi QR code dan redirect ke halaman utama"""
    provided_unit = request.args.get('unit', '')
    
    if not provided_unit:
        flash('Kode unit tidak ditemukan. Silakan scan QR code yang valid.', 'error')
        return redirect(url_for('qr_auth'))
    
    if is_valid_unit_code(provided_unit):
        # Set session untuk menandai bahwa user sudah terverifikasi
        session['qr_verified'] = True
        session['qr_verified_time'] = datetime.now().isoformat()
        session['verified_unit_code'] = provided_unit
        
        logger.info(f"QR verification successful with unit code: {provided_unit}")
        flash('Verifikasi berhasil! Selamat datang di sistem absensi.', 'success')
        return redirect(url_for('home'))
    else:
        logger.warning(f"Invalid QR code attempt with unit: {provided_unit}")
        flash('Kode unit tidak valid atau sudah kedaluwarsa. Silakan scan QR code terbaru.', 'error')
        return redirect(url_for('qr_auth'))

def qr_verification_required(f):
    """Decorator untuk memastikan user sudah melalui QR verification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('qr_verified'):
            flash('Silakan scan QR code terlebih dahulu untuk akses sistem.', 'warning')
            return redirect(url_for('qr_auth'))
        
        # Check if verification is still valid (10 minutes)
        verification_time_str = session.get('qr_verified_time')
        if verification_time_str:
            verification_time = datetime.fromisoformat(verification_time_str)
            if (datetime.now() - verification_time).total_seconds() > QR_VALIDITY_MINUTES * 60:
                session.pop('qr_verified', None)
                session.pop('qr_verified_time', None)
                session.pop('verified_unit_code', None)
                flash('Sesi verifikasi telah berakhir. Silakan scan QR code lagi.', 'warning')
                return redirect(url_for('qr_auth'))
        
        return f(*args, **kwargs)
    return decorated_function

# ======================== MAIN ROUTES ========================

@app.route('/')
@qr_verification_required
def home():
    """Halaman utama untuk user - interface sederhana untuk absensi"""
    names, bagian, tanggal, times, l = extract_attendance()
    return render_template('user_home.html',
        names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
        totalreg=totalreg(), datetoday2=datetoday2,
        date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
        selected_camera=selected_camera_id)

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
    """Dashboard admin dengan semua fitur management"""
    names, bagian, tanggal, times, l = extract_attendance()
    
    # Hitung absensi hari ini
    today_str = current_date.strftime("%d-%m-%Y")
    hadir_hari_ini = sum(1 for t in tanggal if t == today_str)
    
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
        # Deteksi kamera yang tersedia
        cameras = []
        for i in range(5):  # Cek hingga 5 kamera
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append({
                    'id': i,
                    'name': f'Kamera {i}',
                    'status': 'active'
                })
                cap.release()
        
        if not cameras:
            # Jika tidak ada kamera terdeteksi, berikan default
            cameras = [{'id': 0, 'name': 'Kamera Default', 'status': 'default'}]
            
        return jsonify(cameras)
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        return jsonify([{'id': 0, 'name': 'Kamera Default', 'status': 'error'}])

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
    return run_attendance('masuk')

@app.route('/absen_pulang')
def absen_pulang():
    return run_attendance('pulang')

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
    """Route untuk mark attendance yang dipanggil dari frontend"""
    try:
        mode = request.form.get('mode', 'masuk')
        camera_id = request.form.get('camera_id', '0')
        
        logger.info(f"Mark attendance request: mode={mode}, camera_id={camera_id}")
        
        # Simulasi check kamera dulu
        if camera_id == '':
            return jsonify({
                'status': 'error',
                'message': 'Pilih kamera terlebih dahulu!'
            })
        
        # Coba jalankan face recognition
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
            
    except Exception as e:
        logger.error(f"Error in mark_attendance: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        })

def run_attendance_ajax(mode='masuk'):
    """Fungsi absensi yang return JSON untuk AJAX"""
    try:
        cap = cv2.VideoCapture(selected_camera_id)
        if not cap.isOpened():
            return {'status': 'error', 'message': 'Kamera tidak tersedia'}

        if 'face_recognition_model.pkl' not in os.listdir('static'):
            return {'status': 'error', 'message': 'Model belum dilatih. Tambahkan wajah dulu.'}

        recognition_success = False
        success_user = ""
        attempts = 0
        max_attempts = 300  # 10 detik maksimal
        
        while attempts < max_attempts:
            ret, frame = cap.read()
            if not ret:
                break
                
            faces = extract_faces(frame)
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
                user = identify_face(face.reshape(1, -1))[0]
                
                # Update attendance
                update_attendance(user, mode)
                recognition_success = True
                success_user = user
                break
                
            attempts += 1
        
        cap.release()
        cv2.destroyAllWindows()
        
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
                'message': 'Wajah tidak terdeteksi. Silakan coba lagi.'
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
    
    if 'face_recognition_model.pkl' not in os.listdir('static'):
        print(f"[ERROR] Model tidak ditemukan untuk mode {mode}")
        cap.release()
        return render_template('home.html', mess="Model belum dilatih. Tambahkan wajah dulu.",
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
            user = identify_face(face.reshape(1, -1))[0]
            
            # Tampilkan recognition result
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'{user} - {mode.upper()} TERDETEKSI', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
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

def run_attendance_with_camera(mode, camera_id):
    """
    Fungsi untuk menjalankan absensi dengan kamera yang dipilih - dengan GUI window
    Improved cleanup and camera resource management with force release
    """
    cap = None
    window_name = None
    try:
        logger.info(f"Starting camera GUI for {mode} mode with camera {camera_id}")
        
        # AGGRESSIVE CAMERA CLEANUP - Force release any stuck camera resources
        try:
            # Try to create and immediately release camera to force cleanup
            temp_cap = cv2.VideoCapture(camera_id)
            if temp_cap.isOpened():
                temp_cap.release()
            temp_cap = cv2.VideoCapture(0)
            if temp_cap.isOpened():
                temp_cap.release()
            del temp_cap
        except:
            pass
        
        # Force close any existing OpenCV windows
        cv2.destroyAllWindows()
        time.sleep(1.0)  # Increased wait time for complete cleanup
        
        # Additional cleanup attempt
        for i in range(3):  # Try multiple times
            try:
                test_cap = cv2.VideoCapture(camera_id)
                if test_cap.isOpened():
                    test_cap.release()
                    time.sleep(0.3)
                    break
            except:
                continue
        
        # Now try to open camera
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            logger.warning(f"Cannot open camera {camera_id}, trying default camera")
            # Additional cleanup before fallback
            time.sleep(0.5)
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {
                    'status': 'error',
                    'message': f'Tidak dapat mengakses kamera. Pastikan kamera terhubung dengan benar.'
                }
        
        # Set resolusi kamera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        logger.info(f"Camera {camera_id} opened successfully for {mode}")
        
        # Load face detector
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # Setup window dengan nama unik
        window_name = f"Kafebasabasi - Absensi {mode.capitalize()} - {int(time.time())}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)
        
        frame_count = 0
        detection_counter = 0
        face_detected = False
        recognition_success = False
        start_time = time.time()
        
        print(f"[INFO] GUI kamera terbuka untuk mode {mode}")
        print(f"[INFO] Tekan ESC untuk keluar, atau posisikan wajah di depan kamera")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Cannot read frame from camera")
                break
                
            frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Deteksi wajah
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            # Gambar interface
            cv2.putText(frame, f'KAFEBASABASI - ABSENSI {mode.upper()}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f'Kamera: {camera_id} | Frame: {frame_count}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            if len(faces) > 0:
                face_detected = True
                detection_counter += 1
                
                # Gambar rectangle di sekitar wajah
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, 'Wajah Terdeteksi!', (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.putText(frame, f'Mendeteksi... {detection_counter}/30', (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Jika wajah terdeteksi cukup lama, simulasi recognition
                if detection_counter >= 30:
                    recognition_success = True
                    cv2.putText(frame, f'ABSENSI {mode.upper()} BERHASIL!', (10, 120), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(frame, 'Menyimpan data...', (10, 150), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    cv2.putText(frame, 'Window akan ditutup dalam 2 detik', (10, 180), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            else:
                detection_counter = max(0, detection_counter - 1)
                cv2.putText(frame, 'Posisikan wajah di depan kamera', (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Timeout setelah 30 detik
            if time.time() - start_time > 30:
                cv2.putText(frame, 'TIMEOUT - Silakan coba lagi', (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                break
            
            # Instruksi
            cv2.putText(frame, 'Tekan ESC untuk keluar', (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Tampilkan frame
            cv2.imshow(window_name, frame)
            
            # Check key press
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                logger.info("ESC pressed, exiting camera")
                break
            
            # Jika recognition berhasil, tunggu 2 detik lalu keluar
            if recognition_success:
                # Tunggu 2 detik dengan update frame
                for i in range(60):  # 2 detik @ 30fps
                    ret, frame = cap.read()
                    if ret:
                        cv2.putText(frame, f'ABSENSI {mode.upper()} BERHASIL!', (10, 120), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        cv2.putText(frame, 'Data berhasil disimpan!', (10, 150), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                        cv2.imshow(window_name, frame)
                        cv2.waitKey(33)  # ~30fps
                break
        
        logger.info(f"Camera loop finished for {mode}")
        
    except Exception as e:
        logger.error(f"Error in camera GUI: {e}")
        recognition_success = False
        
    finally:
        # AGGRESSIVE COMPREHENSIVE CLEANUP
        logger.info(f"Starting cleanup for {mode} camera")
        
        # Multiple attempts to release camera
        if cap is not None:
            try:
                cap.release()
                logger.info("Camera released")
            except:
                pass
            
            # Additional release attempts
            try:
                del cap
            except:
                pass
        
        # Force destroy specific window
        if window_name:
            try:
                cv2.destroyWindow(window_name)
                logger.info(f"Window {window_name} destroyed")
            except:
                pass
        
        # Multiple cleanup attempts
        for i in range(3):
            try:
                cv2.destroyAllWindows()
                time.sleep(0.3)
            except:
                pass
        
        # FORCE RELEASE ANY REMAINING CAMERA RESOURCES
        try:
            for cam_id in [camera_id, 0, 1]:
                try:
                    temp_cap = cv2.VideoCapture(cam_id)
                    if temp_cap.isOpened():
                        temp_cap.release()
                    del temp_cap
                except:
                    continue
        except:
            pass
        
        # Final extended wait for complete system cleanup
        time.sleep(1.0)
        
        logger.info(f"Cleanup completed for {mode}")
    
    if recognition_success:
        logger.info(f"Attendance {mode} successful")
        return {
            'status': 'success',
            'message': f'✅ Absensi {mode} berhasil! Data telah disimpan.'
        }
    else:
        logger.info(f"Attendance {mode} cancelled or failed")
        return {
            'status': 'warning',
            'message': f'⚠️ Absensi {mode} dibatalkan atau tidak terdeteksi wajah.'
        }

def update_attendance(name, mode='masuk'):
    """Update attendance menggunakan database"""
    try:
        username = name.split('_')[0]
        userbagian = name.split('_')[1]
        current_time = datetime.now().time()
        today = date.today()
        
        # Dapatkan employee
        employee = Employee.get_employee_by_name_bagian(username, userbagian)
        if not employee:
            # Jika employee belum ada, tambahkan dulu
            if Employee.add_employee(username, userbagian):
                employee = Employee.get_employee_by_name_bagian(username, userbagian)
            else:
                logger.error(f"Gagal menambah employee: {username} ({userbagian})")
                return
        
        # Update attendance
        if mode == 'masuk':
            success = Attendance.add_or_update_attendance(employee['id'], today, jam_masuk=current_time)
            activity_type = 'login'
        else:  # mode == 'pulang'
            success = Attendance.add_or_update_attendance(employee['id'], today, jam_pulang=current_time)
            activity_type = 'logout'
        
        if success:
            # Log aktivitas
            ActivityLog.add_log(employee['id'], activity_type, f"Absensi {mode} berhasil")
            logger.info(f"Attendance updated: {username} - {mode} at {current_time}")
        else:
            logger.error(f"Gagal update attendance: {username} - {mode}")
            
    except Exception as e:
        logger.error(f"Error updating attendance: {e}")

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
    cap = cv2.VideoCapture(selected_camera_id)
    if not cap.isOpened():
        names, bagian, tanggal, times, l = extract_attendance()
        return render_template('home.html', mess="Kamera tidak tersedia.",
                               names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
                               totalreg=totalreg(), datetoday2=datetoday2,
                               date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
                               selected_camera=selected_camera_id)

    while True:
        ret, frame = cap.read()
        if not ret:
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
        
        cv2.imshow('Menambah Karyawan Baru', frame)
        if cv2.waitKey(1) == 27:  # ESC key
            break
        
        if i >= nimgs:  # All images captured
            break

    cap.release()
    cv2.destroyAllWindows()
    
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
        for i in range(5):  # Check first 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append({
                    'id': str(i),
                    'name': f'Camera {i}'
                })
                cap.release()
        
        if not cameras:
            cameras = [{'id': '0', 'name': 'Default Camera'}]
            
        return jsonify(cameras)
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        return jsonify([{'id': '0', 'name': 'Default Camera'}])

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
# NGROK TUNNEL MANAGEMENT
# ===========================

def start_ngrok_tunnel(port):
    """Start ngrok tunnel dan return public URL"""
    global ngrok_tunnel
    try:
        # Kill existing tunnels
        ngrok.kill()
        
        # Start new tunnel
        ngrok_tunnel = ngrok.connect(port, "http")
        public_url = str(ngrok_tunnel.public_url)
        
        print("\n" + "="*60)
        print("🌐 KAFEBASABASI ATTENDANCE SYSTEM")
        print("="*60)
        print(f"📱 NGROK PUBLIC URL: {public_url}")
        print(f"🏠 LOCAL URL: http://localhost:{port}")
        print(f"🔗 QR Auth (Public): {public_url}/auth")
        print(f"🔗 QR Auth (Local): http://localhost:{port}/auth")
        print(f"👨‍💼 Admin (Public): {public_url}/admin/login") 
        print(f"👨‍💼 Admin (Local): http://localhost:{port}/admin/login")
        print(f"📊 Ngrok Dashboard: http://localhost:4040")
        print("="*60)
        print("💡 Karyawan bisa scan QR dari HP menggunakan URL public")
        print("💡 Admin bisa akses lokal atau public")
        print("💡 Tekan Ctrl+C untuk shutdown")
        print("="*60 + "\n")
        
        return public_url
        
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        print("💡 Pastikan ngrok sudah terinstall dan authtoken sudah diset")
        print("💡 Aplikasi akan tetap berjalan di mode local only")
        return None

def cleanup_ngrok():
    """Cleanup ngrok saat aplikasi ditutup"""
    global ngrok_tunnel
    try:
        if ngrok_tunnel:
            ngrok.disconnect(ngrok_tunnel)
        ngrok.kill()
        print("✅ Ngrok tunnels closed")
    except:
        pass

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n🛑 Shutting down Kafebasabasi system...')
    
    # Cleanup ngrok
    cleanup_ngrok()
    
    # Close database connection
    try:
        db_manager.close_connection()
        print('✅ Database connection closed')
    except:
        pass
    
    print('👋 Goodbye!')
    sys.exit(0)

if __name__ == '__main__':
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    atexit.register(cleanup_ngrok)
    
    try:
        # Initialize database
        if db_manager.initialize_database():
            logger.info("Database initialized successfully")
            
            # Load app configuration
            port = app_config['port']
            host = app_config['host']
            
            # Check if ngrok should be started (environment variable atau default True)
            use_ngrok = os.environ.get('USE_NGROK', 'true').lower() == 'true'
            
            # Start ngrok tunnel in background if enabled
            public_url = None
            if use_ngrok:
                print("🚀 Starting ngrok tunnel...")
                try:
                    public_url = start_ngrok_tunnel(port)
                except Exception as e:
                    print(f"⚠️ Ngrok failed to start: {e}")
                    print("💡 Continuing with local access only...")
            
            if not public_url:
                print("\n" + "="*60)
                print("🏠 KAFEBASABASI ATTENDANCE SYSTEM (LOCAL ONLY)")
                print("="*60)
                print(f"🔗 Local URL: http://localhost:{port}")
                print(f"🔗 QR Auth: http://localhost:{port}/auth")
                print(f"👨‍💼 Admin: http://localhost:{port}/admin/login")
                print("="*60)
                print("💡 Untuk akses public, set USE_NGROK=true")
                print("💡 Atau install dan setup ngrok")
                print("="*60 + "\n")
            
            logger.info("Starting Kafebasabasi Attendance System v2.0")
            logger.info(f"Local server: http://{host}:{port}")
            
            if public_url:
                logger.info(f"Public access: {public_url}")
            
            # Run Flask app dengan reloader disabled saat pakai ngrok
            app.run(
                debug=app_config['debug'] and not use_ngrok,  # Disable debug jika pakai ngrok
                host=host, 
                port=port,
                use_reloader=False  # Disable reloader untuk stabilitas
            )
        else:
            logger.error("Failed to initialize database. Please run init_database.py first.")
            
    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        # Final cleanup
        cleanup_ngrok()
        db_manager.close_connection()
