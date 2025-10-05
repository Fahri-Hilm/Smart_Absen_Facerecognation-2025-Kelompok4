"""
Script untuk mengosongkan database
Menghapus semua data dari tabel-tabel database
"""

from database import get_db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_database():
    """Mengosongkan semua data dari database"""
    logger.info("=== MENGOSONGKAN DATABASE ===")
    
    db_manager = get_db_manager()
    
    if not db_manager.connect():
        logger.error("❌ Gagal terhubung ke database!")
        return False
    
    try:
        # Nonaktifkan foreign key checks sementara
        db_manager.execute_query("SET FOREIGN_KEY_CHECKS = 0")
        
        # Hapus data dari semua tabel (urutan penting karena foreign key)
        tables_to_clear = [
            'activity_log',      # Hapus dulu karena referensi ke employees
            'attendance',        # Hapus dulu karena referensi ke employees  
            'employees'          # Hapus terakhir
        ]
        
        for table in tables_to_clear:
            try:
                # Cek jumlah data sebelum dihapus
                count_result = db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                count_before = count_result[0]['count'] if count_result else 0
                
                # Hapus semua data
                result = db_manager.execute_query(f"DELETE FROM {table}")
                
                if result is not None:
                    logger.info(f"✅ Tabel '{table}': {count_before} records dihapus")
                else:
                    logger.error(f"❌ Gagal menghapus data dari tabel '{table}'")
                    
            except Exception as e:
                logger.error(f"❌ Error menghapus tabel '{table}': {e}")
        
        # Reset AUTO_INCREMENT untuk semua tabel
        reset_tables = ['employees', 'attendance', 'activity_log']
        for table in reset_tables:
            try:
                db_manager.execute_query(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
                logger.info(f"✅ AUTO_INCREMENT reset untuk tabel '{table}'")
            except Exception as e:
                logger.error(f"❌ Error reset AUTO_INCREMENT untuk '{table}': {e}")
        
        # Aktifkan kembali foreign key checks
        db_manager.execute_query("SET FOREIGN_KEY_CHECKS = 1")
        
        logger.info("🎉 Database berhasil dikosongkan!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error mengosongkan database: {e}")
        return False
    finally:
        db_manager.close_connection()

def verify_empty_database():
    """Verifikasi bahwa database sudah kosong"""
    logger.info("=== VERIFIKASI DATABASE KOSONG ===")
    
    db_manager = get_db_manager()
    
    if not db_manager.connect():
        logger.error("❌ Gagal terhubung ke database!")
        return False
    
    try:
        tables = ['employees', 'attendance', 'activity_log']
        all_empty = True
        
        for table in tables:
            result = db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            count = result[0]['count'] if result else 0
            
            if count == 0:
                logger.info(f"✅ Tabel '{table}': KOSONG (0 records)")
            else:
                logger.warning(f"⚠️  Tabel '{table}': {count} records masih ada")
                all_empty = False
        
        if all_empty:
            logger.info("🎉 Semua tabel sudah kosong!")
        else:
            logger.warning("⚠️  Beberapa tabel masih berisi data")
            
        return all_empty
        
    except Exception as e:
        logger.error(f"❌ Error verifikasi database: {e}")
        return False
    finally:
        db_manager.close_connection()

def main():
    """Fungsi utama"""
    print("🗑️  DATABASE CLEANER")
    print("=" * 50)
    
    # Konfirmasi dari user
    response = input("⚠️  PERINGATAN: Ini akan menghapus SEMUA data dari database!\nApakah Anda yakin? (ketik 'YA' untuk melanjutkan): ").strip()
    
    if response.upper() == 'YA':
        logger.info("User mengkonfirmasi penghapusan database...")
        
        # Kosongkan database
        if clear_database():
            # Verifikasi database kosong
            verify_empty_database()
            logger.info("\n💡 Database sudah dikosongkan. Anda bisa:")
            logger.info("   1. Jalankan 'python init_database.py' untuk menambah sample data")
            logger.info("   2. Atau langsung menambah karyawan melalui aplikasi web")
        else:
            logger.error("❌ Gagal mengosongkan database!")
    else:
        logger.info("❌ Operasi dibatalkan oleh user")

if __name__ == "__main__":
    main()