from database import get_db_manager

db = get_db_manager()

# Check employees
employees = db.execute_query('SELECT * FROM employees')
print('Employees:')
if employees:
    for e in employees:
        print(f'ID: {e["id"]}, Name: {e["name"]}, Bagian: {e["bagian"]}')
else:
    print('No employees found')

# Check attendance
result = db.execute_query('SELECT a.id, e.name, e.bagian, a.tanggal, a.jam_masuk FROM attendance a JOIN employees e ON a.employee_id = e.id')
print('\nAttendance records:')
if result:
    for r in result:
        print(f'Name: {r["name"]}, Bagian: {r["bagian"]}, Tanggal: {r["tanggal"]}')
else:
    print('No records')