import face_recognition
import os
import pickle
import cv2
import numpy as np

image_dir = "images"
known_encodings = []
known_names = []

if not os.path.exists(image_dir):
    print("Error: 'images' folder not found!")
    exit()

# Process each image in the folder
for filename in os.listdir(image_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        name = filename.split("_")[0]  # Extract student name from filename
        image_path = os.path.join(image_dir, filename)

        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            known_encodings.append(face_encodings[0])  # Store only the first face found
            known_names.append(name)
            print(f"✅ Encoded: {filename}")
        else:
            print(f"⚠️ Warning: No face found in {filename} (Skipped)")

# Ensure at least one face was found before saving
if len(known_encodings) == 0:
    print("❌ Error: No valid face encodings found! Ensure images contain clear faces.")
    exit()

# Save encodings
with open("face_encodings.pkl", "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("🎉 Training completed successfully!")
