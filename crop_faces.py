import cv2
import os
import tkinter as tk
from tkinter import filedialog, ttk

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def select_folder():
    global original_folder
    original_folder = filedialog.askdirectory()

def select_output_folder():
    global cropped_folder
    cropped_folder = filedialog.askdirectory()

def crop_faces():
    root.geometry("600x300")
    root.update()
    total_files = len(os.listdir(original_folder))
    progress_bar.config(maximum=total_files)
    for i, filename in enumerate(os.listdir(original_folder)):
        image = cv2.imread(os.path.join(original_folder, filename))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            face_cropped = image[y:y+h, x:x+w]
            face_cropped = cv2.resize(face_cropped, (1080, 1080))
            cv2.imwrite(os.path.join(cropped_folder, "face_" + filename), face_cropped)
        progress_bar.step()
        progress_bar.update()
    success_label.config(text="Faces cropped successfully!")

root = tk.Tk()
root.geometry("600x200")
root.configure(bg="white")
root.title("CutFace")

original_folder_button = tk.Button(root, text="Select original folder", command=select_folder, bg="white", width=20, height=2)
original_folder_button.pack(pady=10)

cropped_folder_button = tk.Button(root, text="Select output folder", command=select_output_folder, bg="white", width=20, height=2)
cropped_folder_button.pack(pady=10)

crop_button = tk.Button(root, text="Crop faces", command=crop_faces, bg="white", width=20, height=2)
crop_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=550, mode="determinate")
progress_bar.pack(pady=10)

success_label = tk.Label(root, text="", bg="white", font=("Helvetica", 14))
success_label.pack(pady=10)

root.mainloop()
