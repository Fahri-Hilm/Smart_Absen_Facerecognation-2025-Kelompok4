#!/usr/bin/env python3
"""
Script untuk menghapus semua data karyawan dan reset database
"""

import os
import shutil
import mysql.connector
from config import Config

def reset_employees():
    print("=" * 50)
    print("🗑️  RESET DATA KARYAWAN ABSENN")
    print("=" * 50)
    
    # 1. Hapus data dari database MySQL
    print("\n[1/4] Menghapus data dari database...")
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        
        # Hapus semua absensi
        cursor.execute("DELETE FROM absensi")
        print(f"   ✓ Tabel absensi dikosongkan")
        
        # Hapus semua karyawan
        cursor.execute("DELETE FROM karyawan")
        print(f"   ✓ Tabel karyawan dikosongkan")
        
        # Reset auto increment
        cursor.execute("ALTER TABLE karyawan AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE absensi AUTO_INCREMENT = 1")
        print(f"   ✓ Auto increment direset")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("   ✓ Database berhasil direset!")
    except Exception as e:
        print(f"   ✗ Error database: {e}")
    
    # 2. Hapus folder foto wajah
    print("\n[2/4] Menghapus foto wajah...")
    faces_dir = "static/faces"
    if os.path.exists(faces_dir):
        for item in os.listdir(faces_dir):
            item_path = os.path.join(faces_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"   ✓ Dihapus: {item}")
        print("   ✓ Semua foto wajah dihapus!")
    else:
        print("   - Folder faces tidak ada")
    
    # 3. Hapus foto profil karyawan
    print("\n[3/4] Menghapus foto profil...")
    photos_dir = "static/employee_photos"
    if os.path.exists(photos_dir):
        for item in os.listdir(photos_dir):
            if item != ".gitkeep":
                item_path = os.path.join(photos_dir, item)
                os.remove(item_path)
                print(f"   ✓ Dihapus: {item}")
        print("   ✓ Semua foto profil dihapus!")
    else:
        print("   - Folder employee_photos tidak ada")
    
    # 4. Hapus face embeddings
    print("\n[4/4] Menghapus face embeddings...")
    embeddings_file = "static/face_embeddings.pkl"
    if os.path.exists(embeddings_file):
        os.remove(embeddings_file)
        print("   ✓ face_embeddings.pkl dihapus!")
    else:
        print("   - File embeddings tidak ada")
    
    # 5. Hapus device registry
    print("\n[Bonus] Menghapus device registry...")
    registry_file = "data/device_registry.json"
    if os.path.exists(registry_file):
        os.remove(registry_file)
        print("   ✓ device_registry.json dihapus!")
    else:
        print("   - File registry tidak ada")
    
    print("\n" + "=" * 50)
    print("✅ RESET SELESAI!")
    print("=" * 50)
    print("\nSekarang Anda bisa mendaftarkan karyawan baru.")
    print("Akses: /admin → Karyawan → Tambah Karyawan")

if __name__ == "__main__":
    confirm = input("\n⚠️  PERINGATAN: Ini akan menghapus SEMUA data karyawan!\nKetik 'HAPUS' untuk konfirmasi: ")
    if confirm == "HAPUS":
        reset_employees()
    else:
        print("❌ Dibatalkan.")
