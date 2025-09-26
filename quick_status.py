from database import get_db_manager
import time

time.sleep(1)  # Wait a moment for database connection
db = get_db_manager()

employees = db.execute_query('SELECT * FROM employees')
print('=== STATUS KARYAWAN TERKINI ===')
print('Total Karyawan:', len(employees) if employees else 0)

if employees:
    for e in employees:
        print(f'- {e["name"]} ({e["bagian"]})')
else:
    print('Tidak ada karyawan')