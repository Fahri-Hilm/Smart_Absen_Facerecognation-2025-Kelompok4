from database import get_db_manager

db = get_db_manager()

print("=== KARYAWAN ===")
employees = db.execute_query('SELECT * FROM employees')
if employees:
    for e in employees:
        print(f'ID: {e["id"]}, Name: {e["name"]}, Bagian: {e["bagian"]}')
    print(f'Total Karyawan: {len(employees)}')
else:
    print('Tidak ada karyawan')
    print('Total Karyawan: 0')

print("\n=== ABSENSI ===")
attendance = db.execute_query('SELECT a.id, e.name, e.bagian, a.tanggal FROM attendance a JOIN employees e ON a.employee_id = e.id')
if attendance:
    for r in attendance:
        print(f'Name: {r["name"]}, Bagian: {r["bagian"]}, Tanggal: {r["tanggal"]}')
    print(f'Total Absensi: {len(attendance)}')
else:
    print('Tidak ada data absensi')
    print('Total Absensi: 0')