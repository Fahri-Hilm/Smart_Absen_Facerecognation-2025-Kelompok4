#!/usr/bin/env python3
"""
Test script untuk memastikan save foto dan auto-training berjalan
"""

import requests
import json
import base64
import os

# Test data
test_employee_id = "1"  # Ganti dengan ID karyawan yang ada
test_photos = []

# Buat dummy base64 image data (1x1 pixel PNG)
dummy_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77yQAAAABJRU5ErkJggg=="

# Buat 10 foto dummy untuk test
for i in range(10):
    test_photos.append(f"data:image/png;base64,{dummy_image_b64}")

# Test data
payload = {
    "employee_id": test_employee_id,
    "photos": test_photos
}

print("🧪 Testing Save Training Photos...")
print(f"Employee ID: {test_employee_id}")
print(f"Photos count: {len(test_photos)}")

# Test API call
try:
    response = requests.post(
        "http://localhost:5001/api/save_training_photos",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Save dan training berhasil!")
    else:
        print("❌ Save atau training gagal!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Pastikan server Flask berjalan di http://localhost:5001")
    print("💡 Dan Anda sudah login sebagai admin")
