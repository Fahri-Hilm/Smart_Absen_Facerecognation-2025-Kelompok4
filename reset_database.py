#!/usr/bin/env python3
"""
Script untuk reset semua data di dat        # Reset auto increment counters
        print("🔄 Resetting auto increment counters...")
        cursor.execute("ALTER TABLE employees AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE attendance AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE activity_log AUTO_INCREMENT = 1")
        print("   ✅ Auto increment counters reset")Menghapus semua data kecuali struktur tabel
"""

import sys
sys.path.append('/home/fj/Desktop/PROJECT/SOFTWARE PROJECT/Absenn')

from database import DatabaseManager
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_all_data():
    """Reset semua data di database (hapus isi data saja, struktur tabel tetap)"""
    try:
        db = DatabaseManager()
        db.connect()
        
        cursor = db.connection.cursor()
        
        print("🗑️  RESET ALL DATABASE DATA")
        print("=" * 50)
        print("⚠️  WARNING: This will delete ALL data!")
        print("   - All employees")
        print("   - All attendance records") 
        print("   - All activity logs")
        print("   - Face recognition model")
        print("   - Face images")
        print()
        
        # Confirm deletion
        confirm = input("Are you sure? Type 'RESET' to confirm: ")
        if confirm != 'RESET':
            print("❌ Reset cancelled")
            return False
        
        print("\n🚀 Starting database reset...")
        
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 1. Delete attendance records first (due to foreign key)
        print("📋 Deleting attendance records...")
        cursor.execute("DELETE FROM attendance")
        affected_attendance = cursor.rowcount
        print(f"   ✅ Deleted {affected_attendance} attendance records")
        
        # 2. Delete activity logs
        print("📝 Deleting activity logs...")
        cursor.execute("DELETE FROM activity_log")
        affected_logs = cursor.rowcount
        print(f"   ✅ Deleted {affected_logs} activity log entries")
        
        # 3. Delete employees
        print("👥 Deleting employees...")
        cursor.execute("DELETE FROM employees")
        affected_employees = cursor.rowcount
        print(f"   ✅ Deleted {affected_employees} employees")
        
        # 4. Reset auto increment counters
        print("🔄 Resetting auto increment counters...")
        cursor.execute("ALTER TABLE employees AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE attendance AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE activity_log AUTO_INCREMENT = 1")
        print("   ✅ Auto increment counters reset")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Commit all changes
        db.connection.commit()
        
        print("\n🧹 Cleaning up files...")
        
        # 5. Delete face recognition model
        import os
        model_path = "static/face_recognition_model.pkl"
        if os.path.exists(model_path):
            os.remove(model_path)
            print(f"   ✅ Deleted face recognition model: {model_path}")
        else:
            print(f"   ℹ️  Face recognition model not found: {model_path}")
        
        # 6. Delete all face images
        faces_dir = "static/faces"
        if os.path.exists(faces_dir):
            import shutil
            for item in os.listdir(faces_dir):
                item_path = os.path.join(faces_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"   ✅ Deleted face folder: {item}")
                elif item.endswith(('.jpg', '.jpeg', '.png')):
                    os.remove(item_path)
                    print(f"   ✅ Deleted face image: {item}")
            print(f"   ✅ Cleaned up faces directory")
        else:
            print(f"   ℹ️  Faces directory not found: {faces_dir}")
        
        cursor.close()
        
        print("\n" + "=" * 50)
        print("✅ DATABASE RESET COMPLETED!")
        print(f"📊 Summary:")
        print(f"   - Employees deleted: {affected_employees}")
        print(f"   - Attendance records deleted: {affected_attendance}")
        print(f"   - Activity logs deleted: {affected_logs}")
        print(f"   - Face data cleaned up")
        print(f"   - Ready for fresh data!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        print(f"❌ Reset failed: {e}")
        return False

def confirm_reset():
    """Interactive confirmation for reset"""
    print("🔍 Current database status:")
    try:
        db = DatabaseManager()
        db.connect()
        cursor = db.connection.cursor()
        
        # Count employees
        cursor.execute("SELECT COUNT(*) as count FROM employees")
        emp_count = cursor.fetchone()['count']
        print(f"   👥 Employees: {emp_count}")
        
        # Count attendance
        cursor.execute("SELECT COUNT(*) as count FROM attendance")
        att_count = cursor.fetchone()['count']
        print(f"   📋 Attendance records: {att_count}")
        
        # Count activity logs
        cursor.execute("SELECT COUNT(*) as count FROM activity_log")
        log_count = cursor.fetchone()['count']
        print(f"   📝 Activity logs: {log_count}")
        
        cursor.close()
        print()
        
        if emp_count == 0 and att_count == 0 and log_count == 0:
            print("ℹ️  Database is already empty!")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking database status: {e}")
        return False

if __name__ == "__main__":
    print("🗃️  KAFEBASABASI DATABASE RESET TOOL")
    print("=" * 50)
    
    if confirm_reset():
        reset_all_data()
    else:
        print("👋 Exiting...")