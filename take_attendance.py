# import cv2
# import face_recognition
# import os
# import pandas as pd
# import pickle
# from datetime import datetime

# # Load trained face encodings
# def load_face_encodings():
#     if not os.path.exists("face_encodings.pkl"):
#         print("Error: No trained face data found. Please train images first.")
#         return None, None

#     with open("face_encodings.pkl", "rb") as f:
#         known_encodings, known_names = pickle.load(f)
#     return known_encodings, known_names

# # Load registered students
# def load_registered_students():
#     if not os.path.exists("students.xlsx"):
#         print("Error: No student registration file found!")
#         return None
    
#     return pd.read_excel("students.xlsx")

# # Mark attendance in the daily file
# def mark_attendance(student_name):
#     date_str = datetime.now().strftime("%Y-%m-%d")
#     attendance_file = f"attendance_{date_str}.xlsx"

#     # Create file if it does not exist
#     if not os.path.exists(attendance_file):
#         df_attendance = pd.DataFrame(columns=["Name", "Roll No", "Enrollment No", "Attendance Time"])
#         df_attendance.to_excel(attendance_file, index=False)

#     df_attendance = pd.read_excel(attendance_file)

#     # Check if student is already marked present
#     if student_name in df_attendance["Name"].values:
#         return False  # Attendance already marked

#     # Get student details
#     student_data = registered_students.loc[registered_students["Name"] == student_name]

#     if student_data.empty:
#         return False  # Student not found

#     new_entry = pd.DataFrame([{
#         "Name": student_name,
#         "Roll No": student_data.iloc[0]["Roll No"],
#         "Enrollment No": student_data.iloc[0]["Enrollment No"],
#         "Attendance Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }])

#     df_attendance = pd.concat([df_attendance, new_entry], ignore_index=True)
#     df_attendance.to_excel(attendance_file, index=False)

#     return True  # Attendance successfully marked

# # Load encodings and students
# known_encodings, known_names = load_face_encodings()
# if known_encodings is None:
#     exit()

# registered_students = load_registered_students()
# if registered_students is None:
#     exit()

# # Initialize camera
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Camera not accessible!")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert frame to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     face_locations = face_recognition.face_locations(rgb_frame, model="hog")  # Faster but less accurate
#     face_encodings_current = face_recognition.face_encodings(rgb_frame, face_locations)

#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_current):
#         matches = face_recognition.compare_faces(known_encodings, face_encoding)
#         face_distances = face_recognition.face_distance(known_encodings, face_encoding)
#         best_match_index = face_distances.argmin() if len(face_distances) > 0 else None

#         name = "Unknown"
#         color = (0, 0, 255)  # Red for unknown

#         if best_match_index is not None and matches[best_match_index]:
#             matched_name = known_names[best_match_index]

#             # Check if student is registered
#             if matched_name in registered_students["Name"].values:
#                 name = matched_name
#                 color = (0, 255, 0)  # Green for registered student

#                 # Mark attendance and show message
#                 if mark_attendance(matched_name):
#                     print(f"✅ Attendance marked successfully for {matched_name}")
#                 else:
#                     print(f"⚠️ {matched_name} is already marked present today.")

#         # Display name on the frame
#         cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#         cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

#     cv2.imshow("Face Recognition Attendance", frame)

#     # Press 'q' to close the camera smoothly
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2
import face_recognition
import os
import pandas as pd
import pickle
from datetime import datetime

# Load trained face encodings
def load_face_encodings():
    if not os.path.exists("face_encodings.pkl"):
        print("Error: No trained face data found. Please train images first.")
        return None, None

    with open("face_encodings.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)
    return known_encodings, known_names

# Load registered students
def load_registered_students():
    if not os.path.exists("students.xlsx"):
        print("Error: No student registration file found!")
        return None
    
    return pd.read_excel("students.xlsx")

# Mark attendance in the daily file
def mark_attendance(student_name):
    date_str = datetime.now().strftime("%Y-%m-%d")
    attendance_file = f"attendance_{date_str}.xlsx"

    # Create file if it does not exist
    if not os.path.exists(attendance_file):
        df_attendance = pd.DataFrame(columns=["Name", "Roll No", "Enrollment No", "Attendance Time"])
        df_attendance.to_excel(attendance_file, index=False)

    df_attendance = pd.read_excel(attendance_file)

    # Check if student is already marked present
    if student_name in df_attendance["Name"].values:
        return False  # Attendance already marked

    # Get student details
    student_data = registered_students.loc[registered_students["Name"] == student_name]

    if student_data.empty:
        return False  # Student not found

    new_entry = pd.DataFrame([{
        "Name": student_name,
        "Roll No": student_data.iloc[0]["Roll No"],
        "Enrollment No": student_data.iloc[0]["Enrollment No"],
        "Attendance Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    df_attendance = pd.concat([df_attendance, new_entry], ignore_index=True)
    df_attendance.to_excel(attendance_file, index=False)

    return True  # Attendance successfully marked

# Load encodings and students
known_encodings, known_names = load_face_encodings()
if known_encodings is None:
    exit()

registered_students = load_registered_students()
if registered_students is None:
    exit()

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not accessible!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame, model="hog")  # Faster but less accurate
    face_encodings_current = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_current):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)  # tolerance is important to capture images
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = face_distances.argmin() if len(face_distances) > 0 else None

        name = "Unknown"
        color = (0, 0, 255)  # Red for unknown

        if best_match_index is not None and matches[best_match_index] and face_distances[best_match_index] < 0.4:
            matched_name = known_names[best_match_index]

            # Check if student is registered
            if matched_name in registered_students["Name"].values:
                name = matched_name
                color = (0, 255, 0)  # Green for registered student

                # Mark attendance and show message
                if mark_attendance(matched_name):
                    print(f"✅ Attendance marked successfully for {matched_name}")
                else:
                    print(f"⚠️ {matched_name} is already marked present today.")

        # Display name on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition Attendance", frame)

    # Press 'q' to close the camera smoothly
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
