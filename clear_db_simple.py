"""
Script sederhana untuk mengosongkan database tanpa konfirmasi
"""

from database import get_db_manager
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def clear_all_data():
    """Mengosongkan semua data langsung"""
    print("🗑️  Mengosongkan database...")
    
    db_manager = get_db_manager()
    
    if not db_manager.connect():
        print("❌ Gagal terhubung ke database!")
        return False
    
    try:
        # Nonaktifkan foreign key checks
        db_manager.execute_query("SET FOREIGN_KEY_CHECKS = 0")
        
        # Hapus data dari semua tabel
        tables = ['activity_log', 'attendance', 'employees']
        
        for table in tables:
            # Cek jumlah data
            count_result = db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            count = count_result[0]['count'] if count_result else 0
            
            # Hapus data
            db_manager.execute_query(f"DELETE FROM {table}")
            print(f"✅ Tabel '{table}': {count} records dihapus")
            
            # Reset AUTO_INCREMENT
            db_manager.execute_query(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
        
        # Aktifkan kembali foreign key checks
        db_manager.execute_query("SET FOREIGN_KEY_CHECKS = 1")
        
        print("🎉 Database berhasil dikosongkan!")
        
        # Verifikasi
        print("\n📊 Verifikasi:")
        for table in ['employees', 'attendance', 'activity_log']:
            result = db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            count = result[0]['count'] if result else 0
            print(f"   - {table}: {count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db_manager.close_connection()

if __name__ == "__main__":
    clear_all_data()