"""
Debug script untuk memeriksa data absensi di database
"""

import os
import sys
sys.path.append(r'C:\Users\FJ\Desktop\SISTEM-ABSENSI-FACE')

from models import Employee, Attendance
from datetime import date, timedelta

print('=== DEBUG TABEL KOSONG PADAHAL DATA MASUK ===')

# 1. Check employees di database
print('\n1. EMPLOYEES DI DATABASE:')
employees = Employee.get_all_employees()
if employees:
    print(f'Total employees: {len(employees)}')
    for emp in employees:
        print(f'  - ID: {emp["id"]}, Name: {emp["name"]}, Bagian: {emp["bagian"]}, Created: {emp.get("created_at", "N/A")}')
else:
    print('Tidak ada employees di database')

# 2. Check ALL attendance data (tidak hanya minggu ini)
print('\n2. SEMUA DATA ATTENDANCE:')
from database import get_db_manager
db = get_db_manager()
all_attendance = db.execute_query("""
    SELECT a.*, e.name, e.bagian 
    FROM attendance a 
    JOIN employees e ON a.employee_id = e.id 
    ORDER BY a.tanggal DESC, a.created_at DESC
""")

if all_attendance:
    print(f'Total attendance records: {len(all_attendance)}')
    for att in all_attendance:
        print(f'  - ID: {att["id"]}, Employee: {att["name"]} ({att["bagian"]})')
        print(f'    Tanggal: {att["tanggal"]}, Masuk: {att["jam_masuk"]}, Pulang: {att["jam_pulang"]}')
        print(f'    Created: {att.get("created_at", "N/A")}')
        print()
else:
    print('Tidak ada attendance records sama sekali')

# 3. Check attendance minggu ini
print('\n3. ATTENDANCE DATA MINGGU INI:')
current_date = date.today()
start_of_week = current_date - timedelta(days=current_date.weekday())
end_of_week = start_of_week + timedelta(days=6)

print(f'Date range: {start_of_week} to {end_of_week}')
print(f'Today: {current_date}')

attendance_week = Attendance.get_weekly_attendance(start_of_week, end_of_week)
if attendance_week:
    print(f'Total attendance minggu ini: {len(attendance_week)}')
    for att in attendance_week:
        print(f'  - {att["name"]} ({att["bagian"]}) - {att["tanggal"]}')
        print(f'    Masuk: {att["jam_masuk"]}, Pulang: {att["jam_pulang"]}')
else:
    print('Tidak ada attendance records minggu ini')

# 4. Check attendance hari ini
print('\n4. ATTENDANCE DATA HARI INI:')
today_attendance = db.execute_query("""
    SELECT a.*, e.name, e.bagian 
    FROM attendance a 
    JOIN employees e ON a.employee_id = e.id 
    WHERE a.tanggal = %s
    ORDER BY a.created_at DESC
""", (current_date,))

if today_attendance:
    print(f'Total attendance hari ini: {len(today_attendance)}')
    for att in today_attendance:
        print(f'  - {att["name"]} ({att["bagian"]}) - {att["tanggal"]}')
        print(f'    Masuk: {att["jam_masuk"]}, Pulang: {att["jam_pulang"]}')
else:
    print('Tidak ada attendance records hari ini')

# 5. Test extract_attendance function
print('\n5. TEST EXTRACT_ATTENDANCE FUNCTION:')
try:
    sys.path.append(r'C:\Users\FJ\Desktop\SISTEM-ABSENSI-FACE')
    from app import extract_attendance
    names, bagian, tanggal, times, l = extract_attendance()
    print(f'Extract result: {l} records')
    if l > 0:
        for i in range(l):
            print(f'  - {names[i]} ({bagian[i]}) - {tanggal[i]}')
            print(f'    Times: {times[i]}')
    else:
        print('Extract_attendance returned empty')
except Exception as e:
    print(f'Error testing extract_attendance: {e}')

print('\n=== KESIMPULAN ===')
print(f'Total employees: {len(employees) if employees else 0}')
print(f'Total attendance records: {len(all_attendance) if all_attendance else 0}')
print(f'Attendance minggu ini: {len(attendance_week) if attendance_week else 0}')
print(f'Attendance hari ini: {len(today_attendance) if today_attendance else 0}')

if all_attendance and not attendance_week:
    print('\n⚠️ MASALAH DITEMUKAN: Ada data attendance tapi tidak masuk filter minggu ini')
    print('Kemungkinan masalah dengan date range atau timezone')
elif not all_attendance:
    print('\n❌ MASALAH: Tidak ada data attendance sama sekali di database')
    print('Data absensi tidak tersimpan ke database')
else:
    print('\n✅ Data attendance tersedia')