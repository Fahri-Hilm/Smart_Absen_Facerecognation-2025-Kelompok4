"""
Database Models untuk Sistem Absensi Karyawan
Berisi class-class untuk mengelola data karyawan dan absensi
"""

from database import get_db_manager
from datetime import datetime, date, time
import logging

logger = logging.getLogger(__name__)

class Employee:
    """Model untuk data karyawan"""
    
    @staticmethod
    def add_employee(name, bagian):
        """Menambah karyawan baru"""
        try:
            db = get_db_manager()
            query = "INSERT INTO employees (name, bagian) VALUES (%s, %s)"
            result = db.execute_query(query, (name, bagian))
            if result:
                logger.info(f"Karyawan {name} ({bagian}) berhasil ditambahkan")
                return True
            return False
        except Exception as e:
            logger.error(f"Gagal menambah karyawan: {e}")
            return False
    
    @staticmethod
    def get_employee_by_name_bagian(name, bagian):
        """Mendapatkan data karyawan berdasarkan nama dan bagian"""
        try:
            db = get_db_manager()
            query = "SELECT * FROM employees WHERE name = %s AND bagian = %s"
            result = db.execute_query(query, (name, bagian))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Gagal mendapatkan data karyawan: {e}")
            return None
    
    @staticmethod
    def get_all_employees():
        """Mendapatkan semua data karyawan"""
        try:
            db = get_db_manager()
            query = "SELECT * FROM employees ORDER BY name"
            return db.execute_query(query)
        except Exception as e:
            logger.error(f"Gagal mendapatkan data karyawan: {e}")
            return []
    
    @staticmethod
    def employee_exists(name, bagian):
        """Cek apakah karyawan sudah ada"""
        employee = Employee.get_employee_by_name_bagian(name, bagian)
        return employee is not None


class Attendance:
    """Model untuk data absensi"""
    
    @staticmethod
    def add_or_update_attendance(employee_id, tanggal, jam_masuk=None, jam_pulang=None):
        """Menambah atau update data absensi"""
        try:
            db = get_db_manager()
            
            # Cek apakah sudah ada record untuk hari ini
            existing = Attendance.get_attendance_by_employee_date(employee_id, tanggal)
            
            if existing:
                # Update existing record
                updates = []
                params = []
                
                if jam_masuk and not existing['jam_masuk']:
                    updates.append("jam_masuk = %s")
                    params.append(jam_masuk)
                
                if jam_pulang and not existing['jam_pulang']:
                    updates.append("jam_pulang = %s")
                    params.append(jam_pulang)
                
                if updates:
                    # Hitung total jam kerja jika ada jam masuk dan pulang
                    if jam_pulang and existing['jam_masuk']:
                        total_jam = Attendance.calculate_work_hours(existing['jam_masuk'], jam_pulang)
                        updates.append("total_jam_kerja = %s")
                        params.append(total_jam)
                    elif jam_masuk and existing['jam_pulang']:
                        total_jam = Attendance.calculate_work_hours(jam_masuk, existing['jam_pulang'])
                        updates.append("total_jam_kerja = %s")
                        params.append(total_jam)
                    
                    params.extend([employee_id, tanggal])
                    query = f"UPDATE attendance SET {', '.join(updates)} WHERE employee_id = %s AND tanggal = %s"
                    result = db.execute_query(query, params)
                    return result > 0
            else:
                # Insert new record
                query = """
                INSERT INTO attendance (employee_id, tanggal, jam_masuk, jam_pulang, total_jam_kerja) 
                VALUES (%s, %s, %s, %s, %s)
                """
                total_jam = None
                if jam_masuk and jam_pulang:
                    total_jam = Attendance.calculate_work_hours(jam_masuk, jam_pulang)
                
                result = db.execute_query(query, (employee_id, tanggal, jam_masuk, jam_pulang, total_jam))
                return result > 0
                
        except Exception as e:
            logger.error(f"Gagal menambah/update absensi: {e}")
            return False
    
    @staticmethod
    def get_attendance_by_employee_date(employee_id, tanggal):
        """Mendapatkan data absensi berdasarkan employee_id dan tanggal"""
        try:
            db = get_db_manager()
            query = "SELECT * FROM attendance WHERE employee_id = %s AND tanggal = %s"
            result = db.execute_query(query, (employee_id, tanggal))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Gagal mendapatkan data absensi: {e}")
            return None
    
    @staticmethod
    def get_weekly_attendance(start_date, end_date):
        """Mendapatkan data absensi mingguan"""
        try:
            db = get_db_manager()
            query = """
            SELECT a.*, e.name, e.bagian 
            FROM attendance a 
            JOIN employees e ON a.employee_id = e.id 
            WHERE a.tanggal BETWEEN %s AND %s 
            ORDER BY a.tanggal DESC, e.name
            """
            return db.execute_query(query, (start_date, end_date))
        except Exception as e:
            logger.error(f"Gagal mendapatkan data absensi mingguan: {e}")
            return []
    
    @staticmethod
    def get_today_attendance():
        """Mendapatkan data absensi hari ini"""
        today = date.today()
        return Attendance.get_weekly_attendance(today, today)
    
    @staticmethod
    def calculate_work_hours(jam_masuk, jam_pulang):
        """Menghitung total jam kerja"""
        try:
            if isinstance(jam_masuk, str):
                jam_masuk = datetime.strptime(jam_masuk, "%H:%M:%S").time()
            if isinstance(jam_pulang, str):
                jam_pulang = datetime.strptime(jam_pulang, "%H:%M:%S").time()
            
            # Convert to datetime untuk perhitungan
            today = date.today()
            dt_masuk = datetime.combine(today, jam_masuk)
            dt_pulang = datetime.combine(today, jam_pulang)
            
            # Hitung selisih
            if dt_pulang > dt_masuk:
                diff = dt_pulang - dt_masuk
                total_seconds = int(diff.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return time(hours, minutes, seconds)
            
            return None
        except Exception as e:
            logger.error(f"Gagal menghitung jam kerja: {e}")
            return None


class ActivityLog:
    """Model untuk log aktivitas"""
    
    @staticmethod
    def add_log(employee_id, activity_type, description=""):
        """Menambah log aktivitas"""
        try:
            db = get_db_manager()
            query = "INSERT INTO activity_log (employee_id, activity_type, description) VALUES (%s, %s, %s)"
            result = db.execute_query(query, (employee_id, activity_type, description))
            return result > 0
        except Exception as e:
            logger.error(f"Gagal menambah log aktivitas: {e}")
            return False
    
    @staticmethod
    def get_recent_logs(limit=50):
        """Mendapatkan log aktivitas terbaru"""
        try:
            db = get_db_manager()
            query = """
            SELECT al.*, e.name, e.bagian 
            FROM activity_log al 
            LEFT JOIN employees e ON al.employee_id = e.id 
            ORDER BY al.created_at DESC 
            LIMIT %s
            """
            return db.execute_query(query, (limit,))
        except Exception as e:
            logger.error(f"Gagal mendapatkan log aktivitas: {e}")
            return []