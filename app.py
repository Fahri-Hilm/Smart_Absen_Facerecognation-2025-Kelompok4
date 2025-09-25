import cv2
import os
import csv
from flask import Flask, request, render_template
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib

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
        
        names = []
        bagian = []
        tanggal = []
        times = []
        
        for record in attendance_data:
            names.append(record['name'])
            bagian.append(record['bagian'])
            tanggal.append(record['tanggal'].strftime("%d-%m-%Y"))
            
            jam_masuk = record['jam_masuk'].strftime("%H:%M:%S") if record['jam_masuk'] else '-'
            jam_pulang = record['jam_pulang'].strftime("%H:%M:%S") if record['jam_pulang'] else '-'
            total_jam = record['total_jam_kerja'].strftime("%H:%M:%S") if record['total_jam_kerja'] else '-'
            
            times.append((jam_masuk, jam_pulang, total_jam))
        
        return names, bagian, tanggal, times, len(attendance_data)
        
    except Exception as e:
        logger.error(f"Error extracting attendance: {e}")
        return [], [], [], [], 0

@app.route('/')
def home():
    names, bagian, tanggal, times, l = extract_attendance()
    return render_template('home.html',
        names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
        totalreg=totalreg(), datetoday2=datetoday2,
        date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
        selected_camera=selected_camera_id, mess=None)

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

def run_attendance(mode='masuk'):
    print(f"[DEBUG] Mulai absensi ({mode}) dengan kamera ID: {selected_camera_id}")
    cap = cv2.VideoCapture(selected_camera_id)
    if not cap.isOpened():
        return render_template('home.html', mess="Kamera tidak tersedia.",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return render_template('home.html', mess="Model belum dilatih. Tambahkan wajah dulu.",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = extract_faces(frame)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            user = identify_face(face.reshape(1, -1))[0]
            update_attendance(user, mode)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'{user} - {mode.upper()}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.putText(frame, f'Mode: {mode.upper()} - Tekan ESC untuk keluar', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow(f"Absensi {mode.capitalize()}", frame)
        if cv2.waitKey(1) == 27:  # ESC key
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return home()

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

if __name__ == '__main__':
    try:
        # Initialize database on startup
        if db_manager.initialize_database():
            logger.info("Database initialized successfully")
            app.run(debug=app_config['debug'], host=app_config['host'], port=app_config['port'])
        else:
            logger.error("Failed to initialize database. Please run init_database.py first.")
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    finally:
        # Close database connection
        db_manager.close_connection()
