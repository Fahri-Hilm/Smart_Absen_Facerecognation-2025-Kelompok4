"""
Script untuk test koneksi database dan verifikasi data
"""

from database import get_db_manager
from models import Employee, Attendance, ActivityLog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test koneksi database"""
    logger.info("=== TEST KONEKSI DATABASE ===")
    
    db_manager = get_db_manager()
    
    if db_manager.connect():
        logger.info("✅ Koneksi database berhasil!")
        return True
    else:
        logger.error("❌ Koneksi database gagal!")
        return False

def show_database_info():
    """Tampilkan informasi database"""
    logger.info("=== INFORMASI DATABASE ===")
    
    db_manager = get_db_manager()
    
    try:
        # Test query untuk setiap tabel
        employees = db_manager.execute_query("SELECT COUNT(*) as count FROM employees")
        attendance = db_manager.execute_query("SELECT COUNT(*) as count FROM attendance") 
        activity_log = db_manager.execute_query("SELECT COUNT(*) as count FROM activity_log")
        
        logger.info(f"📊 Jumlah karyawan: {employees[0]['count'] if employees else 0}")
        logger.info(f"📊 Jumlah record absensi: {attendance[0]['count'] if attendance else 0}")
        logger.info(f"📊 Jumlah log aktivitas: {activity_log[0]['count'] if activity_log else 0}")
        
        # Tampilkan daftar karyawan
        all_employees = Employee.get_all_employees()
        if all_employees:
            logger.info("\n👥 DAFTAR KARYAWAN:")
            for emp in all_employees:
                logger.info(f"   - {emp['name']} ({emp['bagian']}) - ID: {emp['id']}")
        
        # Tampilkan absensi hari ini
        today_attendance = Attendance.get_today_attendance()
        if today_attendance:
            logger.info("\n📅 ABSENSI HARI INI:")
            for att in today_attendance:
                jam_masuk = att['jam_masuk'].strftime("%H:%M:%S") if att['jam_masuk'] else '-'
                jam_pulang = att['jam_pulang'].strftime("%H:%M:%S") if att['jam_pulang'] else '-'
                logger.info(f"   - {att['name']} ({att['bagian']}): {jam_masuk} - {jam_pulang}")
        else:
            logger.info("\n📅 Belum ada absensi hari ini")
            
    except Exception as e:
        logger.error(f"❌ Error getting database info: {e}")

def test_database_operations():
    """Test operasi database dasar"""
    logger.info("=== TEST OPERASI DATABASE ===")
    
    try:
        # Test 1: Tambah karyawan test
        test_name = "TestUser"
        test_bagian = "testing"
        
        if not Employee.employee_exists(test_name, test_bagian):
            if Employee.add_employee(test_name, test_bagian):
                logger.info("✅ Test tambah karyawan berhasil")
            else:
                logger.error("❌ Test tambah karyawan gagal")
        else:
            logger.info("ℹ️  Test user sudah ada")
        
        # Test 2: Ambil data karyawan
        employee = Employee.get_employee_by_name_bagian(test_name, test_bagian)
        if employee:
            logger.info(f"✅ Test ambil data karyawan berhasil: {employee['name']}")
        
            # Test 3: Tambah log aktivitas
            if ActivityLog.add_log(employee['id'], 'add_employee', 'Test log aktivitas'):
                logger.info("✅ Test tambah log aktivitas berhasil")
            else:
                logger.error("❌ Test tambah log aktivitas gagal")
        
        # Test 4: Ambil log aktivitas terbaru
        recent_logs = ActivityLog.get_recent_logs(5)
        if recent_logs:
            logger.info(f"✅ Test ambil log aktivitas berhasil: {len(recent_logs)} records")
        
    except Exception as e:
        logger.error(f"❌ Error testing database operations: {e}")

def main():
    """Fungsi utama"""
    print("🔍 DATABASE VERIFICATION TOOL")
    print("=" * 50)
    
    try:
        # Test koneksi
        if test_database_connection():
            # Tampilkan info database
            show_database_info()
            
            # Test operasi database
            test_database_operations()
            
            logger.info("\n🎉 Semua test database berhasil!")
            logger.info("💡 Database siap digunakan untuk aplikasi absensi")
        else:
            logger.error("❌ Test database gagal!")
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        # Tutup koneksi
        db_manager = get_db_manager()
        db_manager.close_connection()

if __name__ == "__main__":
    main()