import os
import cv2
import pandas as pd
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

# Function to save student data and capture images
def save_student():
    name = entry_name.get().strip()
    roll_no = entry_roll.get().strip()
    enrollment = entry_enrollment.get().strip()
    
    if not name or not roll_no or not enrollment:
        messagebox.showerror("Error", "Please fill all fields")
        return

    # Save student details to Excel
    data = {"Name": [name], "Roll No": [roll_no], "Enrollment No": [enrollment]}
    df = pd.DataFrame(data)
    
    if os.path.exists("students.xlsx"):
        df_existing = pd.read_excel("students.xlsx")
        df = pd.concat([df_existing, df], ignore_index=True)
    
    df.to_excel("students.xlsx", index=False)
    messagebox.showinfo("Success", "Student registered successfully!")

    # Capture student images
    capture_images(name)

# Function to capture student images
def capture_images(name):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        messagebox.showerror("Error", "Camera not accessible!")
        return
    
    count = 0
    img_path = None  # Store last captured image path

    os.makedirs("images", exist_ok=True)

    while count < 5:
        ret, frame = cam.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            continue  # If no face detected, try again
        
        for (x, y, w, h) in faces:
            count += 1
            face_img = frame[y:y+h, x:x+w]
            img_path = f"images/{name}_{count}.jpg"
            cv2.imwrite(img_path, face_img)

        cv2.imshow("Capturing Images", frame)
        cv2.waitKey(500)

    cam.release()
    cv2.destroyAllWindows()

    if img_path:
        show_image(img_path)
        messagebox.showinfo("Success", "Student images captured successfully!")
    else:
        messagebox.showerror("Error", "No face detected! Try again.")

# Function to display last captured image
def show_image(img_path):
    img = Image.open(img_path)
    img = img.resize((150, 150), Image.LANCZOS)  # Fixed the ANITALIAS issue
    img = ImageTk.PhotoImage(img)
    lbl_image.config(image=img)
    lbl_image.image = img  # Keep reference

# Function to train images
def train_images():
    if os.path.exists("train_faces.py"):
        messagebox.showinfo("Training", "Training images... Please wait.")
        subprocess.run(["python", "train_faces.py"])
        messagebox.showinfo("Training Completed", "Images trained successfully!")
    else:
        messagebox.showerror("Error", "train_faces.py not found!")

# Function to take automatic attendance
def take_attendance():
    script_path = os.path.abspath("take_attendance.py")  # Get absolute pathS

    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"File not found: {script_path}")
        return

    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error running take_attendance.py:\n{e}")

# Function to check student attendance sheet
def check_sheet():
    if os.path.exists("students.xlsx"):
        os.system("start excel students.xlsx")  # Opens in Excel (Windows)
    else:
        messagebox.showerror("Error", "No student sheet found!")

# Function to check today's attendance
def check_todays_attendance():
    date_str = datetime.now().strftime("%Y-%m-%d")
    attendance_file = f"attendance_{date_str}.xlsx"
    
    if os.path.exists(attendance_file):
        os.system(f"start excel {attendance_file}")  # Opens today's attendance file
    else:
        messagebox.showerror("Error", "Today's attendance sheet not found!")

# Create main GUI window
root = tk.Tk()
root.title("Student Registration")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Title Label
tk.Label(root, text="Student Registration", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=10)

# Input Fields
frame_inputs = tk.Frame(root, bg="#f5f5f5")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Name:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame_inputs, width=30)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(frame_inputs, text="Roll No:", font=("Arial", 12), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5)
entry_roll = tk.Entry(frame_inputs, width=30)
entry_roll.grid(row=1, column=1, pady=5)

tk.Label(frame_inputs, text="Enrollment No:", font=("Arial", 12), bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5)
entry_enrollment = tk.Entry(frame_inputs, width=30)
entry_enrollment.grid(row=2, column=1, pady=5)

# Buttons (Aligned Horizontally)
frame_buttons = tk.Frame(root, bg="#f5f5f5")
frame_buttons.pack(pady=10)

btn_save = tk.Button(frame_buttons, text="Save & Capture", font=("Arial", 12), bg="#88B6F2", fg="black", command=save_student, width=15)
btn_save.grid(row=0, column=0, padx=5)

btn_train = tk.Button(frame_buttons, text="Train Images", font=("Arial", 12), bg="#04B2D9", fg="white", command=train_images, width=15)
btn_train.grid(row=0, column=1, padx=5)

btn_attendance = tk.Button(frame_buttons, text="Take Attendance", font=("Arial", 12), bg="#B6DBF2", fg="black", command=take_attendance, width=18)
btn_attendance.grid(row=0, column=2, padx=5)

# Check Sheet Buttons
frame_check_sheet = tk.Frame(root, bg="#f5f5f5")
frame_check_sheet.pack(pady=10)

btn_check_sheet = tk.Button(frame_check_sheet, text="Check Student Sheet", font=("Arial", 12), bg="#79AEF2", fg="black", command=check_sheet, width=20)
btn_check_sheet.grid(row=0, column=0, padx=5)

btn_check_attendance = tk.Button(frame_check_sheet, text="Check Today's Attendance", font=("Arial", 12), bg="#79AEF2", fg="black", command=check_todays_attendance, width=20)
btn_check_attendance.grid(row=0, column=1, padx=5)

# Image Preview
lbl_image = tk.Label(root, bg="#f5f5f5")
lbl_image.pack(pady=10)

# Run Tkinter main loop
root.mainloop()
