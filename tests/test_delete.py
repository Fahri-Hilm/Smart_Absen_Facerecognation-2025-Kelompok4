from database import get_db_manager
from models import Employee
from datetime import datetime

# Simulate delete request
employee_name = "Faju"
employee_bagian = "Staff"  
tanggal = "26-09-2025"  # Today's date in DD-MM-YYYY format

print(f"Testing delete with: Name={employee_name}, Bagian={employee_bagian}, Tanggal={tanggal}")

# Parse tanggal like in the delete function
tanggal_obj = datetime.strptime(tanggal, "%d-%m-%Y").date()
print(f"Parsed date object: {tanggal_obj}")

# Check if employee exists
employee = Employee.get_employee_by_name_bagian(employee_name, employee_bagian)
print(f"Employee found: {employee}")

if employee:
    db = get_db_manager()
    # Check if attendance record exists
    check_query = "SELECT * FROM attendance WHERE employee_id = %s AND tanggal = %s"
    existing_record = db.execute_query(check_query, (employee['id'], tanggal_obj))
    print(f"Existing attendance record: {existing_record}")
    
    if existing_record:
        print("Record found! Delete would succeed.")
    else:
        print("Record NOT found! This is why delete fails.")
else:
    print("Employee not found! This is why delete fails.")