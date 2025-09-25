"""
Script untuk inisialisasi database MySQL
Jalankan script ini untuk membuat database dan tabel yang diperlukan
"""

from database import get_db_manager
from models import Employee, Attendance, ActivityLog
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_database():
    """Inisialisasi database dan tabel"""
    logger.info("=== INISIALISASI DATABASE SISTEM ABSENSI ===")
    
    # Inisialisasi database manager
    db_manager = get_db_manager()
    
    # Inisialisasi database
    if db_manager.initialize_database():
        logger.info("✅ Database berhasil diinisialisasi!")
        
        # Test koneksi dengan query sederhana
        result = db_manager.execute_query("SELECT COUNT(*) as count FROM employees")
        if result:
            logger.info(f"✅ Test koneksi berhasil. Jumlah karyawan: {result[0]['count']}")
        
        return True
    else:
        logger.error("❌ Gagal inisialisasi database!")
        return False

def add_sample_data():
    """Menambah data sample untuk testing (opsional)"""
    logger.info("Menambah data sample...")
    
    # Sample employees
    sample_employees = [
        ("Fahri", "karyawan"),
        ("Faju", "karyawan"), 
        ("Folva", "karyawan"),
        ("Max", "staff"),
        ("Maxi", "staff")
    ]
    
    for name, bagian in sample_employees:
        if not Employee.employee_exists(name, bagian):
            if Employee.add_employee(name, bagian):
                logger.info(f"✅ Sample employee added: {name} ({bagian})")
            else:
                logger.error(f"❌ Failed to add sample employee: {name} ({bagian})")
        else:
            logger.info(f"ℹ️  Employee already exists: {name} ({bagian})")

def main():
    """Fungsi utama"""
    try:
        # Inisialisasi database
        if initialize_database():
            
            # Tanya user apakah ingin menambah sample data
            response = input("\nApakah Anda ingin menambah data sample karyawan? (y/n): ").lower().strip()
            if response in ['y', 'yes', 'ya']:
                add_sample_data()
            
            logger.info("\n🎉 Setup database selesai!")
            logger.info("Anda sekarang bisa menjalankan aplikasi dengan: python app.py")
            
        else:
            logger.error("❌ Setup database gagal!")
            
    except KeyboardInterrupt:
        logger.info("\n⏹️  Setup dibatalkan oleh user")
    except Exception as e:
        logger.error(f"❌ Error tidak terduga: {e}")
    finally:
        # Tutup koneksi database
        db_manager = get_db_manager()
        db_manager.close_connection()

if __name__ == "__main__":
    main()