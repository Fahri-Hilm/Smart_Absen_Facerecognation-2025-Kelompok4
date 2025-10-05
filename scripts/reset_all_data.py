"""
Script untuk mengosongkan semua data dan reset sistem absensi
Menghapus:
- Semua data dari database MySQL
- Semua foto wajah
- Model face recognition
- File CSV attendance
"""

import os
import shutil
import glob
from database import get_db_manager
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def clear_database():
    """Hapus semua data dari database"""
    try:
        logger.info("🗄️ Menghapus semua data dari database...")
        db = get_db_manager()
        
        # Hapus data dalam urutan yang benar untuk menghindari foreign key constraints
        logger.info("Menghapus data activity_log...")
        db.execute_query("DELETE FROM activity_log")
        
        logger.info("Menghapus data attendance...")
        db.execute_query("DELETE FROM attendance")
        
        logger.info("Menghapus data employees...")
        db.execute_query("DELETE FROM employees")
        
        # Reset auto increment
        logger.info("Reset auto increment counters...")
        db.execute_query("ALTER TABLE activity_log AUTO_INCREMENT = 1")
        db.execute_query("ALTER TABLE attendance AUTO_INCREMENT = 1")
        db.execute_query("ALTER TABLE employees AUTO_INCREMENT = 1")
        
        logger.info("✅ Database berhasil dikosongkan!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error clearing database: {e}")
        return False

def clear_face_images():
    """Hapus semua foto wajah"""
    try:
        logger.info("📸 Menghapus semua foto wajah...")
        faces_dir = "static/faces"
        
        if os.path.exists(faces_dir):
            # Hapus semua folder karyawan
            for folder in os.listdir(faces_dir):
                folder_path = os.path.join(faces_dir, folder)
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
                    logger.info(f"Menghapus folder: {folder}")
        
        logger.info("✅ Semua foto wajah berhasil dihapus!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error clearing face images: {e}")
        return False

def clear_face_model():
    """Hapus model face recognition"""
    try:
        logger.info("🤖 Menghapus model face recognition...")
        model_file = "static/face_recognition_model.pkl"
        
        if os.path.exists(model_file):
            os.remove(model_file)
            logger.info("Model face recognition dihapus")
        
        logger.info("✅ Model face recognition berhasil dihapus!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error clearing face model: {e}")
        return False

def clear_attendance_files():
    """Hapus file CSV attendance"""
    try:
        logger.info("📊 Menghapus file CSV attendance...")
        attendance_dir = "Attendance"
        
        if os.path.exists(attendance_dir):
            # Hapus semua file CSV
            csv_files = glob.glob(os.path.join(attendance_dir, "*.csv"))
            for csv_file in csv_files:
                os.remove(csv_file)
                logger.info(f"Menghapus file: {os.path.basename(csv_file)}")
        
        logger.info("✅ File CSV attendance berhasil dihapus!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error clearing attendance files: {e}")
        return False

def verify_clean_state():
    """Verifikasi bahwa semua data sudah bersih"""
    try:
        logger.info("🔍 Memverifikasi status pembersihan...")
        
        # Check database
        db = get_db_manager()
        employees_count = db.execute_query("SELECT COUNT(*) as count FROM employees")[0]['count']
        attendance_count = db.execute_query("SELECT COUNT(*) as count FROM attendance")[0]['count']
        activity_count = db.execute_query("SELECT COUNT(*) as count FROM activity_log")[0]['count']
        
        logger.info(f"Database - Employees: {employees_count}, Attendance: {attendance_count}, Activity Log: {activity_count}")
        
        # Check face images
        faces_dir = "static/faces"
        face_folders = 0
        if os.path.exists(faces_dir):
            face_folders = len([f for f in os.listdir(faces_dir) if os.path.isdir(os.path.join(faces_dir, f))])
        
        logger.info(f"Face images - Folders: {face_folders}")
        
        # Check model
        model_exists = os.path.exists("static/face_recognition_model.pkl")
        logger.info(f"Face model - Exists: {model_exists}")
        
        # Check CSV files
        csv_count = len(glob.glob("Attendance/*.csv"))
        logger.info(f"CSV files - Count: {csv_count}")
        
        # Summary
        is_clean = (employees_count == 0 and attendance_count == 0 and 
                   activity_count == 0 and face_folders == 0 and 
                   not model_exists and csv_count == 0)
        
        if is_clean:
            logger.info("✅ Sistem berhasil dibersihkan! Siap untuk data baru.")
        else:
            logger.warning("⚠️ Masih ada data yang tersisa.")
        
        return is_clean
        
    except Exception as e:
        logger.error(f"❌ Error verifying clean state: {e}")
        return False

def main():
    """Main function untuk reset semua data"""
    logger.info("🚀 === RESET SISTEM ABSENSI KARYAWAN ===")
    logger.info("Akan menghapus SEMUA data: database, foto, model, dan file CSV")
    
    # Konfirmasi
    confirm = input("\n⚠️ PERINGATAN: Ini akan menghapus SEMUA data!\nKetik 'YES' untuk melanjutkan: ")
    
    if confirm.upper() != 'YES':
        logger.info("❌ Reset dibatalkan.")
        return
    
    logger.info("\n🗑️ Memulai proses pembersihan...")
    
    # Execute cleaning steps
    steps = [
        ("Database", clear_database),
        ("Face Images", clear_face_images),
        ("Face Model", clear_face_model),
        ("Attendance Files", clear_attendance_files)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        logger.info(f"\n--- {step_name} ---")
        if step_func():
            success_count += 1
        else:
            logger.error(f"Gagal membersihkan {step_name}")
    
    logger.info(f"\n📊 Selesai! {success_count}/{len(steps)} langkah berhasil")
    
    # Verify
    logger.info("\n--- Verifikasi ---")
    verify_clean_state()
    
    logger.info("\n🎉 Reset sistem selesai!")
    logger.info("Anda sekarang bisa menambah data karyawan baru melalui web interface.")

if __name__ == "__main__":
    main()