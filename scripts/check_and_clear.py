"""
Script untuk melihat dan menghapus data karyawan yang terdaftar
"""

from database import get_db_manager
from models import Employee

def show_all_employees():
    """Tampilkan semua karyawan yang terdaftar"""
    print("👥 DAFTAR KARYAWAN TERDAFTAR:")
    print("=" * 50)
    
    db_manager = get_db_manager()
    if not db_manager.connect():
        print("❌ Gagal terhubung ke database!")
        return
    
    try:
        # Ambil semua karyawan
        employees = db_manager.execute_query("SELECT * FROM employees ORDER BY name")
        
        if employees:
            print(f"📊 Total: {len(employees)} karyawan")
            print()
            for i, emp in enumerate(employees, 1):
                print(f"{i}. {emp['name']} ({emp['bagian']}) - ID: {emp['id']}")
                print(f"   Created: {emp['created_at']}")
                print()
        else:
            print("📭 Tidak ada karyawan terdaftar")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db_manager.close_connection()

def delete_all_employees():
    """Hapus semua karyawan"""
    print("🗑️  MENGHAPUS SEMUA KARYAWAN...")
    
    db_manager = get_db_manager()
    if not db_manager.connect():
        print("❌ Gagal terhubung ke database!")
        return
    
    try:
        # Nonaktifkan foreign key checks
        db_manager.execute_query("SET FOREIGN_KEY_CHECKS = 0")
        
        # Hapus semua data
        tables = ['activity_log', 'attendance', 'employees']
        
        for table in tables:
            count_result = db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            count = count_result[0]['count'] if count_result else 0
            
            if count > 0:
                db_manager.execute_query(f"DELETE FROM {table}")
                db_manager.execute_query(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
                print(f"✅ Tabel '{table}': {count} records dihapus")
            else:
                print(f"ℹ️  Tabel '{table}': sudah kosong")
        
        # Aktifkan kembali foreign key checks
        db_manager.execute_query("SET FOREIGN_KEY_CHECKS = 1")
        
        print("🎉 Semua karyawan berhasil dihapus!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db_manager.close_connection()

if __name__ == "__main__":
    print("🔍 CEK & HAPUS KARYAWAN TERDAFTAR")
    print("=" * 50)
    
    # Tampilkan daftar karyawan
    show_all_employees()
    
    # Konfirmasi hapus
    response = input("\n❓ Apakah Anda ingin menghapus SEMUA karyawan? (ketik 'YA'): ").strip()
    
    if response.upper() == 'YA':
        delete_all_employees()
        print("\n✅ Selesai! Database sudah bersih.")
    else:
        print("❌ Operasi dibatalkan")