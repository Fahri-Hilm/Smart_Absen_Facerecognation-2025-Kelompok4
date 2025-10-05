import requests

try:
    # Test endpoint get_attendance_data yang mengandung totalreg
    url = "http://127.0.0.1:5001/get_attendance_data"
    response = requests.get(url)
    data = response.json()
    
    print("=== RESPONSE GET_ATTENDANCE_DATA ===")
    print(f"Status: {data.get('status')}")
    if 'data' in data:
        print(f"Total dari endpoint: {data['data'].get('totalreg')}")
        print(f"Total absensi: {data['data'].get('total')}")
        print(f"Names: {data['data'].get('names')}")
    
    # Test endpoint get_employees 
    url2 = "http://127.0.0.1:5001/get_employees"
    response2 = requests.get(url2)
    data2 = response2.json()
    
    print("\n=== RESPONSE GET_EMPLOYEES ===")
    print(f"Status: {data2.get('status')}")
    print(f"Employees: {data2.get('employees')}")
    
except Exception as e:
    print(f"Error: {e}")