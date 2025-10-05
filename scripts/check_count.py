from database import get_db_manager

db = get_db_manager()
result = db.execute_query('SELECT COUNT(*) as count FROM attendance')
print(f'Total attendance records: {result[0]["count"] if result else 0}')

# Show all records
all_records = db.execute_query('SELECT a.id, e.name, e.bagian, a.tanggal FROM attendance a JOIN employees e ON a.employee_id = e.id')
if all_records:
    print("All records:")
    for r in all_records:
        print(f'ID: {r["id"]}, Name: {r["name"]}, Bagian: {r["bagian"]}, Tanggal: {r["tanggal"]}')
else:
    print("No attendance records found")