#!/usr/bin/env python3
"""
Script untuk memperbaiki dan menghitung ulang total jam kerja
yang null atau kosong di database
"""

import sys
sys.path.append('/home/fj/Desktop/PROJECT/SOFTWARE PROJECT/Absenn')

from database import DatabaseManager
from models import Employee, Attendance
from datetime import date, datetime, timedelta, time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_total_jam_kerja():
    """Menghitung ulang total jam kerja untuk semua record yang memiliki jam masuk dan pulang"""
    try:
        db = DatabaseManager()
        db.connect()
        
        # Query untuk mendapatkan semua attendance yang memiliki jam_masuk dan jam_pulang tapi total_jam_kerja NULL
        query = """
        SELECT id, employee_id, tanggal, jam_masuk, jam_pulang, total_jam_kerja 
        FROM attendance 
        WHERE jam_masuk IS NOT NULL 
        AND jam_pulang IS NOT NULL 
        AND total_jam_kerja IS NULL
        """
        
        cursor = db.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        
        print(f"🔍 Found {len(records)} records dengan total_jam_kerja NULL")
        print()
        
        fixed_count = 0
        for record in records:
            attendance_id = record['id']
            employee_id = record['employee_id']
            tanggal = record['tanggal']
            jam_masuk = record['jam_masuk']
            jam_pulang = record['jam_pulang']
            
            # Get employee info
            emp_query = "SELECT name, bagian FROM employees WHERE id = %s"
            cursor.execute(emp_query, (employee_id,))
            employee = cursor.fetchone()
            emp_name = employee['name'] if employee else f"ID-{employee_id}"
            emp_bagian = employee['bagian'] if employee else "Unknown"
            
            print(f"📝 Processing: {emp_name} ({emp_bagian}) - {tanggal}")
            print(f"   ⏰ Masuk: {jam_masuk}")
            print(f"   ⏰ Pulang: {jam_pulang}")
            
            # Calculate total jam kerja
            total_jam = Attendance.calculate_work_hours(jam_masuk, jam_pulang)
            
            if total_jam:
                # Convert timedelta to readable format
                total_seconds = int(total_jam.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                
                print(f"   ✅ Calculated: {hours} jam {minutes} menit")
                
                # Update database
                update_query = "UPDATE attendance SET total_jam_kerja = %s WHERE id = %s"
                cursor.execute(update_query, (total_jam, attendance_id))
                db.connection.commit()
                
                fixed_count += 1
            else:
                print(f"   ❌ Failed to calculate (jam pulang <= jam masuk)")
            
            print()
        
        print(f"✅ Successfully fixed {fixed_count} records")
        
        # Show updated results
        print("📊 Updated Attendance Records:")
        employees = Employee.get_all_employees()
        today = date.today()
        
        for emp in employees:
            attendance = Attendance.get_attendance_by_employee_date(emp['id'], today)
            if attendance and attendance.get('jam_masuk'):
                total_jam = attendance.get('total_jam_kerja')
                if total_jam:
                    total_seconds = int(total_jam.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    total_display = f"{hours}h {minutes}m"
                else:
                    total_display = "NULL"
                
                print(f"👤 {emp['name']} ({emp['bagian']}): {total_display}")
        
        cursor.close()
        
    except Exception as e:
        logger.error(f"Error fixing total jam kerja: {e}")
        return False

if __name__ == "__main__":
    fix_total_jam_kerja()