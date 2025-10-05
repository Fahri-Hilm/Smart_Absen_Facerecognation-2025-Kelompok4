from app import totalreg
from models import Employee

print("=== TEST TOTALREG FUNCTION ===")

# Test langsung function totalreg()
total = totalreg()
print(f"Hasil totalreg(): {total}")

# Test langsung get_all_employees()
employees = Employee.get_all_employees()
print(f"Hasil Employee.get_all_employees(): {employees}")
print(f"Length: {len(employees) if employees else 0}")

# Test manual count dari database langsung
from database import get_db_manager
db = get_db_manager()
direct_count = db.execute_query("SELECT COUNT(*) as count FROM employees")
print(f"Direct database count: {direct_count[0]['count'] if direct_count else 0}")

# Test folder faces
import os
try:
    face_folders = os.listdir('static/faces')
    print(f"Folder faces count: {len(face_folders)}")
except:
    print("Folder faces tidak ada atau error")