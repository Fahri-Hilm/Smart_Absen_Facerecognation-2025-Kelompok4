# Konfigurasi Database MySQL untuk Laragon
# Database configuration for employee attendance system

import os

# Konfigurasi Database MariaDB (Devilbox default settings)
DATABASE_CONFIG = {
    'host': '127.0.0.1',  # Devilbox host
    'port': 3306,
    'user': 'root',
    'password': '',  # Devilbox default: no password for root
    'database': 'absensi_karyawan_db',  # Nama database baru
    'charset': 'utf8mb4',
    'autocommit': True
}

# Konfigurasi aplikasi
APP_CONFIG = {
    'secret_key': 'absensi-karyawan-secret-key-2025',
    'debug': True,
    'host': '0.0.0.0',  # Ubah ke 0.0.0.0 agar bisa diakses dari jaringan lokal
    'port': 5001
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