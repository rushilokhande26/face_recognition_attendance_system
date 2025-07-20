import cv2
import os

IMAGE_PATH = "images"  # Folder where images will be saved
STUDENT_NAME = input("Enter student name: ")  # Get student name

# Create a folder for the student
student_folder = os.path.join(IMAGE_PATH, STUDENT_NAME)
os.makedirs(student_folder, exist_ok=True)  

cap = cv2.VideoCapture(0)
count = 0

print("Capturing images... Look at the camera.")
while count < 30:  # Capture 30 images
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not access camera.")
        break

    img_path = os.path.join(student_folder, f"image_{count + 1}.jpg")
    cv2.imwrite(img_path, frame)  # Save image
    count += 1

    cv2.imshow("Capturing Images", frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):  # Press 'q' to quit early
        break

cap.release()
cv2.destroyAllWindows()
print(f"Captured {count} images for {STUDENT_NAME}.")
