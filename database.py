"""
Database Manager untuk Sistem Absensi Karyawan
Menggunakan PyMySQL untuk koneksi ke MySQL database
"""

import pymysql
import pymysql.cursors
from datetime import datetime, date
import logging
from config import get_db_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.config = get_db_config()
        self.connection = None
    
    def connect(self):
        """Membuat koneksi ke database MySQL"""
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset'],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=self.config['autocommit']
            )
            logger.info("Berhasil terhubung ke database MySQL")
            return True
        except Exception as e:
            logger.error(f"Gagal terhubung ke database: {e}")
            return False
    
    def create_database_if_not_exists(self):
        """Membuat database jika belum ada"""
        try:
            # Koneksi tanpa specify database untuk membuat database baru
            temp_connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                charset=self.config['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            
            with temp_connection.cursor() as cursor:
                # Buat database jika belum ada
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                logger.info(f"Database '{self.config['database']}' berhasil dibuat atau sudah ada")
            
            temp_connection.close()
            return True
        except Exception as e:
            logger.error(f"Gagal membuat database: {e}")
            return False
    
    def create_tables(self):
        """Membuat tabel-tabel yang diperlukan"""
        try:
            with self.connection.cursor() as cursor:
                # Tabel karyawan
                create_employees_table = """
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    bagian VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_employee (name, bagian)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                # Tabel absensi
                create_attendance_table = """
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    employee_id INT NOT NULL,
                    tanggal DATE NOT NULL,
                    jam_masuk TIME NULL,
                    jam_pulang TIME NULL,
                    total_jam_kerja TIME NULL,
                    status ENUM('hadir', 'tidak_hadir', 'terlambat') DEFAULT 'hadir',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_attendance (employee_id, tanggal)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                # Tabel log aktivitas (opsional, untuk tracking)
                create_activity_log_table = """
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    employee_id INT NULL,
                    activity_type ENUM('login', 'logout', 'add_employee', 'face_recognition') NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                # Eksekusi pembuatan tabel
                cursor.execute(create_employees_table)
                cursor.execute(create_attendance_table)
                cursor.execute(create_activity_log_table)
                
                logger.info("Semua tabel berhasil dibuat")
                return True
                
        except Exception as e:
            logger.error(f"Gagal membuat tabel: {e}")
            return False
    
    def close_connection(self):
        """Menutup koneksi database"""
        if self.connection:
            self.connection.close()
            logger.info("Koneksi database ditutup")
    
    def get_connection(self):
        """Mendapatkan koneksi database"""
        if not self.connection or not self.connection.open:
            if not self.connect():
                return None
        return self.connection
    
    def execute_query(self, query, params=None):
        """Eksekusi query dengan parameter"""
        try:
            connection = self.get_connection()
            if not connection:
                return None
                
            with connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    return cursor.rowcount
        except Exception as e:
            logger.error(f"Gagal eksekusi query: {e}")
            return None
    
    def initialize_database(self):
        """Inisialisasi lengkap database"""
        logger.info("Memulai inisialisasi database...")
        
        # 1. Buat database jika belum ada
        if not self.create_database_if_not_exists():
            return False
        
        # 2. Koneksi ke database
        if not self.connect():
            return False
        
        # 3. Buat tabel-tabel
        if not self.create_tables():
            return False
        
        logger.info("Inisialisasi database selesai!")
        return True


# Instance global database manager
db_manager = DatabaseManager()

def get_db_manager():
    """Mendapatkan instance database manager"""
    return db_manager