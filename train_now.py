#!/usr/bin/env python3
"""Script untuk training model InsightFace"""

import sys
import os

# Set PYTHONPATH
sys.path.insert(0, '/home/fj/.local/lib/python3.12/site-packages')

os.chdir('/home/fj/Desktop/PROJECT/Campus/SOFTWARE PROJECT/Absenn')

# List faces folder
faces_dir = 'static/faces'
if os.path.exists(faces_dir):
    print("Faces folder contents:")
    for item in os.listdir(faces_dir):
        item_path = os.path.join(faces_dir, item)
        if os.path.isdir(item_path):
            files = os.listdir(item_path)
            print(f"  {item}/: {len(files)} files")
else:
    print("Faces folder not found!")
    sys.exit(1)

# Train model
print("\nTraining model...")
try:
    from face_recognition_insightface import train_insightface_model
    result = train_insightface_model()
    print(f"Training result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Check if model file created
model_file = 'static/face_embeddings.pkl'
if os.path.exists(model_file):
    print(f"\n✅ Model file created: {model_file}")
    print(f"   Size: {os.path.getsize(model_file)} bytes")
else:
    print(f"\n❌ Model file not found: {model_file}")
