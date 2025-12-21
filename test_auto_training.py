#!/usr/bin/env python3
"""
Test script untuk memastikan auto-training berjalan saat save foto
"""

import sys
import os
sys.path.append('.')

from models import Employee
from app import train_model
import base64
import json

print("🧪 Test Auto-Training Saat Save Foto")
print("=" * 50)

# 1. Cek karyawan yang ada
employees = Employee.get_all_employees()
print(f"Total karyawan di database: {len(employees)}")

if not employees:
    print("❌ Tidak ada karyawan di database")
    sys.exit(1)

# Ambil karyawan pertama untuk test
test_employee = employees[0]
employee_id = test_employee['id']
nik = test_employee['nik']
name = test_employee['name']

print(f"Test employee: {name} (ID: {employee_id}, NIK: {nik})")

# 2. Simulasi save foto dengan auto-training
faces_dir = f'static/faces/{nik}'
os.makedirs(faces_dir, exist_ok=True)

# Dummy 1x1 pixel PNG (base64)
dummy_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77yQAAAABJRU5ErkJggg=="

print(f"Saving photos to: {faces_dir}")

# Simulasi save 10 foto
saved_count = 0
for i in range(1, 11):
    try:
        img_data = base64.b64decode(dummy_b64)
        with open(f'{faces_dir}/auto_test_{i}.jpg', 'wb') as f:
            f.write(img_data)
        saved_count += 1
        print(f"📸 Saved photo {i} for {name}")
    except Exception as e:
        print(f"❌ Error saving photo {i}: {e}")

print(f"✅ SAVED {saved_count} photos for {name}")

# 3. Test auto-training (simulasi yang terjadi di endpoint)
print(f"🚀 STARTING AUTO TRAINING for {name}...")

train_success = False
train_error = ""
try:
    train_success = train_model()
    if train_success:
        print(f"✅ AUTO TRAINING SUCCESS: {name} dengan {saved_count} foto")
    else:
        print(f"❌ AUTO TRAINING FAILED: {name}")
        train_error = "Training model gagal"
except Exception as e:
    print(f"❌ AUTO TRAINING ERROR: {e}")
    train_error = str(e)

# 4. Response message (seperti di endpoint)
response_message = f'✅ {name} berhasil disimpan dengan {saved_count} foto!'
if train_success:
    response_message += ' Model berhasil di-training dan siap untuk absensi!'
else:
    response_message += f' ⚠️ Training gagal: {train_error}'

print("\n" + "="*50)
print("📋 HASIL TEST AUTO-TRAINING:")
print(f"Message: {response_message}")
print(f"Training Success: {train_success}")
print(f"Saved Photos: {saved_count}")
print("="*50)

# 5. Cek file model
model_file = "static/face_embeddings.pkl"
if os.path.exists(model_file):
    stat = os.stat(model_file)
    print(f"✅ Model file exists: {model_file}")
    print(f"   Size: {stat.st_size} bytes")
    print(f"   Modified: {stat.st_mtime}")
else:
    print(f"❌ Model file not found: {model_file}")

print("\n🎉 Test auto-training selesai!")
print("Cek log server untuk melihat detail proses training.")
