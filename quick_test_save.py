#!/usr/bin/env python3
"""
Quick test untuk save foto dan auto-training
"""

import sys
import os
sys.path.append('.')

from models import Employee
from app import train_model
import base64

print("🧪 Quick Test Save & Training")
print("=" * 40)

# 1. Cek karyawan yang ada
employees = Employee.get_all_employees()
print(f"Total karyawan: {len(employees)}")

if not employees:
    print("❌ Tidak ada karyawan di database")
    sys.exit(1)

# Ambil karyawan pertama untuk test
test_employee = employees[0]
employee_id = test_employee['id']
nik = test_employee['nik']
name = test_employee['name']

print(f"Test employee: {name} (ID: {employee_id}, NIK: {nik})")

# 2. Buat folder dan save dummy photos
faces_dir = f'static/faces/{nik}'
os.makedirs(faces_dir, exist_ok=True)

# Dummy 1x1 pixel PNG
dummy_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77yQAAAABJRU5ErkJggg=="

print(f"Saving photos to: {faces_dir}")

saved_count = 0
for i in range(1, 11):  # Save 10 photos
    try:
        img_data = base64.b64decode(dummy_b64)
        with open(f'{faces_dir}/test_face_{i}.jpg', 'wb') as f:
            f.write(img_data)
        saved_count += 1
    except Exception as e:
        print(f"Error saving photo {i}: {e}")

print(f"✅ Saved {saved_count} photos")

# 3. Test training
print("🚀 Starting training...")
try:
    success = train_model()
    if success:
        print("✅ Training berhasil!")
    else:
        print("❌ Training gagal!")
except Exception as e:
    print(f"❌ Training error: {e}")

print("\n🎉 Test selesai!")
print(f"Cek folder: {faces_dir}")
print("Cek file model: static/face_embeddings.pkl")
