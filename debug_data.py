"""
Debug script untuk memeriksa masalah Total Terdaftar vs Tabel Kosong
"""

import os
import sys
sys.path.append(r'C:\Users\FJ\Desktop\SISTEM-ABSENSI-FACE')

from models import Employee, Attendance
from datetime import date, timedelta

print('=== DEBUG TOTAL TERDAFTAR vs TABEL KOSONG ===')

# 1. Check employees di database
print()
print('1. EMPLOYEES DI DATABASE:')
employees = Employee.get_all_employees()
if employees:
    print(f'Total employees: {len(employees)}')
    for emp in employees:
        print(f'  - ID: {emp["id"]}, Name: {emp["name"]}, Bagian: {emp["bagian"]}')
else:
    print('Tidak ada employees di database')

# 2. Check folder faces
print()
print('2. FOLDER FACES:')
faces_dir = r'C:\Users\FJ\Desktop\SISTEM-ABSENSI-FACE\static\faces'
if os.path.exists(faces_dir):
    folders = [f for f in os.listdir(faces_dir) if os.path.isdir(os.path.join(faces_dir, f))]
    print(f'Total folders: {len(folders)}')
    for folder in folders:
        print(f'  - {folder}')
else:
    print('Folder faces tidak ada')

# 3. Check attendance data minggu ini
print()
print('3. ATTENDANCE DATA MINGGU INI:')
current_date = date.today()
start_of_week = current_date - timedelta(days=current_date.weekday())
end_of_week = start_of_week + timedelta(days=6)

print(f'Date range: {start_of_week} to {end_of_week}')
attendance_data = Attendance.get_weekly_attendance(start_of_week, end_of_week)
if attendance_data:
    print(f'Total attendance records: {len(attendance_data)}')
    for att in attendance_data:
        print(f'  - {att["name"]} ({att["bagian"]}) - {att["tanggal"]}')
else:
    print('Tidak ada attendance records minggu ini')

print()
print('=== KESIMPULAN ===')
emp_count = len(employees) if employees else 0
folder_count = len(folders) if 'folders' in locals() else 0
att_count = len(attendance_data) if attendance_data else 0

print(f'Employee count: {emp_count}')
print(f'Face folders: {folder_count}')
print(f'Attendance records: {att_count}')

print()
print('MASALAH YANG DITEMUKAN:')
if emp_count > 0 and att_count == 0:
    print('❌ Ada employees tapi tidak ada attendance records')
    print('   Solusi: Karyawan belum melakukan absensi')
elif emp_count == 0 and folder_count > 0:
    print('❌ Ada folder faces tapi tidak ada employees di database')
    print('   Solusi: Data tidak konsisten, perlu sinkronisasi')
elif emp_count > 0 and folder_count == 0:
    print('❌ Ada employees di database tapi tidak ada folder faces')
    print('   Solusi: Foto belum diambil atau terhapus')
else:
    print('✅ Data konsisten')