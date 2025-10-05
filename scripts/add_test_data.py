from database import get_db_manager
from datetime import date, time

db = get_db_manager()

# Add test data
try:
    result1 = db.execute_query(
        'INSERT INTO attendance (employee_id, tanggal, jam_masuk, jam_pulang, total_jam_kerja) VALUES (%s, %s, %s, %s, %s)', 
        (1, date.today(), time(8, 0), time(17, 0), time(9, 0))
    )
    print(f"Insert result 1: {result1}")
    
    result2 = db.execute_query(
        'INSERT INTO attendance (employee_id, tanggal, jam_masuk, jam_pulang, total_jam_kerja) VALUES (%s, %s, %s, %s, %s)', 
        (6, date.today(), time(9, 0), time(18, 0), time(9, 0))
    )
    print(f"Insert result 2: {result2}")
    
    print("Test data added successfully")
except Exception as e:
    print(f"Error adding data: {e}")