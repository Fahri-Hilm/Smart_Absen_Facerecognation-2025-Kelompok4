# Konfigurasi Database MySQL untuk Laragon
# Database configuration for employee attendance system

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi Database MariaDB (with environment variables)
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'absensi_karyawan_db'),
    'charset': 'utf8mb4',
    'autocommit': True
}

# Konfigurasi aplikasi
APP_CONFIG = {
    'secret_key': os.getenv('SECRET_KEY', 'dev-key-change-in-production'),
    'debug': os.getenv('FLASK_DEBUG', 'True') == 'True',
    'host': os.getenv('FLASK_HOST', '0.0.0.0'),
    'port': int(os.getenv('FLASK_PORT', 5001))
}

# Konfigurasi face recognition
FACE_CONFIG = {
    'cascade_file': 'haarcascade_frontalface_default.xml',
    'model_file': 'static/face_recognition_model.pkl',
    'faces_dir': 'static/faces',
    'num_images': 10,
    'face_size': (50, 50)
}

# Konfigurasi file dan folder
FOLDERS = {
    'attendance': 'Attendance',
    'static': 'static',
    'faces': 'static/faces',
    'templates': 'templates'
}

# Fungsi untuk mendapatkan konfigurasi berdasarkan environment
def get_db_config():
    """
    Mendapatkan konfigurasi database.
    Bisa dimodifikasi untuk environment berbeda (development, production)
    """
    return DATABASE_CONFIG.copy()

def get_app_config():
    """
    Mendapatkan konfigurasi aplikasi Flask
    """
    return APP_CONFIG.copy()