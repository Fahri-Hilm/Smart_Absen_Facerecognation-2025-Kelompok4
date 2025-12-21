#!/usr/bin/env python3
"""
Script untuk menghapus semua data karyawan dan foto training
"""
import os
import shutil
import pymysql
from config import DATABASE_CONFIG

def reset_all_data():
    print("🗑️ Menghapus semua data karyawan dan foto training...")
    
    # 1. Hapus semua foto training
    faces_dir = "static/faces"
    if os.path.exists(faces_dir):
        shutil.rmtree(faces_dir)
        print(f"✅ Folder {faces_dir} dihapus")
    
    # 2. Hapus file model training
    model_files = [
        "static/face_embeddings.pkl",
        "static/employee_photos"
    ]
    
    for file_path in model_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            print(f"✅ {file_path} dihapus")
    
    # 3. Reset database
    try:
        connection = pymysql.connect(
            host=DATABASE_CONFIG['host'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            database=DATABASE_CONFIG['database'],
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Hapus semua data karyawan
            cursor.execute("DELETE FROM employees")
            deleted_employees = cursor.rowcount
            
            # Hapus semua data absensi
            cursor.execute("DELETE FROM attendance")
            deleted_attendance = cursor.rowcount
            
            # Reset auto increment
            cursor.execute("ALTER TABLE employees AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE attendance AUTO_INCREMENT = 1")
            
        connection.commit()
        connection.close()
        
        print(f"✅ Database direset:")
        print(f"   - {deleted_employees} karyawan dihapus")
        print(f"   - {deleted_attendance} record absensi dihapus")
        
    except Exception as e:
        print(f"❌ Error database: {e}")
    
    # 4. Buat ulang folder faces
    os.makedirs(faces_dir, exist_ok=True)
    print(f"✅ Folder {faces_dir} dibuat ulang")
    
    print("\n🎉 Reset selesai! Semua data karyawan dan foto training telah dihapus.")
    print("💡 Sekarang Anda bisa input data karyawan baru.")

if __name__ == "__main__":
    confirm = input("⚠️ Yakin ingin menghapus SEMUA data karyawan dan foto? (y/N): ")
    if confirm.lower() == 'y':
        reset_all_data()
    else:
        print("❌ Reset dibatalkan")
