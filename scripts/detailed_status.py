from database import get_db_manager

db = get_db_manager()

print("=== DETAIL STATUS DATABASE ===")
employees = db.execute_query('SELECT * FROM employees')

if employees:
    print(f"Total Karyawan di Database: {len(employees)}")
    print("\nDetail Karyawan:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. ID: {emp['id']}, Name: '{emp['name']}', Bagian: '{emp['bagian']}'")
        print(f"   Created: {emp['created_at']}")
        print(f"   Updated: {emp['updated_at']}")
        print()
else:
    print("Database kosong - tidak ada karyawan")

# Cek juga folder faces
import os
if os.path.exists('static/faces'):
    face_folders = os.listdir('static/faces')
    print(f"Folder faces berisi: {len(face_folders)} folder")
    for folder in face_folders:
        print(f"  - {folder}")
else:
    print("Folder static/faces tidak ada")