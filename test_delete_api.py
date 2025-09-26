import requests

# Test delete endpoint
url = "http://127.0.0.1:5001/delete_attendance"

# Test data - using the known working values from our test
data = {
    'name': 'fj',
    'bagian': 'Karyawan',
    'tanggal': '26-09-2025'
}

print(f"Sending delete request for: {data}")

try:
    response = requests.post(url, data=data)
    print(f"Response status: {response.status_code}")
    print(f"Response JSON: {response.json()}")
except Exception as e:
    print(f"Error: {e}")