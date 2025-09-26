import sys
sys.path.append(r'C:\Users\FJ\Desktop\SISTEM-ABSENSI-FACE')

from database import get_db_manager
from models import Employee, Attendance
from datetime import date, timedelta

print('=== DEBUGGING ATTENDANCE DATA ===')

# Check database connection
db = get_db_manager()
print('Database connected successfully')

# Check employees
employees = Employee.get_all_employees()
print(f'Total employees: {len(employees) if employees else 0}')

# Check ALL attendance records
all_att = db.execute_query('SELECT COUNT(*) as count FROM attendance')
print(f'Total attendance records in DB: {all_att[0]["count"] if all_att else 0}')

# Check today
today = date.today()
today_att = db.execute_query('SELECT COUNT(*) as count FROM attendance WHERE tanggal = %s', (today,))
print(f'Attendance records today ({today}): {today_att[0]["count"] if today_att else 0}')

# Check this week
start_week = today - timedelta(days=today.weekday())
end_week = start_week + timedelta(days=6)
week_att = db.execute_query('SELECT COUNT(*) as count FROM attendance WHERE tanggal BETWEEN %s AND %s', (start_week, end_week))
print(f'Attendance records this week ({start_week} to {end_week}): {week_att[0]["count"] if week_att else 0}')

# Show recent records
recent = db.execute_query('SELECT * FROM attendance ORDER BY created_at DESC LIMIT 5')
print(f'Recent 5 attendance records:')
for r in recent:
    print(f'  - ID:{r["id"]}, Employee:{r["employee_id"]}, Date:{r["tanggal"]}, In:{r["jam_masuk"]}, Out:{r["jam_pulang"]}')

# Test extract function
print('\n=== TESTING EXTRACT FUNCTION ===')
try:
    from app import extract_attendance
    names, bagian, tanggal, times, l = extract_attendance()
    print(f'Extract function returned {l} records')
    if l > 0:
        for i in range(l):
            print(f'  - {names[i]} ({bagian[i]}) on {tanggal[i]}')
except Exception as e:
    print(f'Error in extract_attendance: {e}')