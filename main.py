import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Function to open Register Student window
def register_student():
    subprocess.run(["python", "register_student.py"])

# Function to train images
def train_images():
    messagebox.showinfo("Training", "Training images... Please wait.")
    subprocess.run(["python", "train_faces.py"])
    messagebox.showinfo("Training Completed", "Images trained successfully!")

# Function to take automatic attendance
def take_attendance():
    messagebox.showinfo("Attendance", "Opening camera for automatic attendance...")
    subprocess.run(["python", "take_attendance.py"])

# Function to check attendance sheet
def check_attendance():
    if os.path.exists("attendance.xlsx"):
        os.system("start excel attendance.xlsx")  # Opens attendance file in Excel
    else:
        messagebox.showerror("Error", "Attendance file not found!")

# Create main GUI window
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("500x400")
root.configure(bg="lightblue")

# Add a title label
label_title = tk.Label(root, text="Face Recognition Attendance System", font=("Arial", 16, "bold"), bg="lightblue")
label_title.pack(pady=20)

# Add buttons
btn_register = tk.Button(root, text="Register New Student", font=("Arial", 12), bg="orange", fg="white", command=register_student)
btn_register.pack(pady=10)

btn_train = tk.Button(root, text="Train Images", font=("Arial", 12), bg="green", fg="white", command=train_images)
btn_train.pack(pady=10)

btn_attendance = tk.Button(root, text="Take Automatic Attendance", font=("Arial", 12), bg="blue", fg="white", command=take_attendance)
btn_attendance.pack(pady=10)

btn_check_sheet = tk.Button(root, text="Check Attendance Sheet", font=("Arial", 12), bg="purple", fg="white", command=check_attendance)
btn_check_sheet.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
