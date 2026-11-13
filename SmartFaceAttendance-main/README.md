# Smart Face Attendance System

A Flask-based web application that automates attendance management using Face Recognition technology. The system captures student faces, trains facial encodings, recognizes registered students in real time, and records attendance automatically.

---

## Features

- 📸 Capture student face images using a webcam
- 🧠 Train face encodings for recognition
- 👤 Recognize registered students in real time
- ✅ Mark attendance automatically
- 📊 Store attendance records in Excel files
- 🌐 User-friendly web interface built with Flask
- 🎥 Attractive video background UI

---

## Tech Stack

- Python
- Flask
- OpenCV
- face_recognition
- NumPy
- Pandas
- OpenPyXL
- HTML, CSS, JavaScript

---

## Project Structure

```text
SmartFaceAttendance/
│
├── app.py                     # Main Flask application
├── capture_face.py           # Capture face images
├── train_faces.py            # Train facial encodings
├── attendance_face.py        # Face recognition & attendance
│
├── templates/
│   ├── index.html
│   ├── capture.html
│   ├── train.html
│   ├── attendance.html
│   └── attendance_table.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── videos/
│       └── background.mp4
│
├── trained_faces/
│
├── dataset/                  # Generated after capturing faces
│
├── students.xlsx             # Student information
├── attendance.xlsx           # Attendance records
│
└── .gitignore
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/saru-d/SmartFaceAttendance.git
cd SmartFaceAttendance
```

### Create a virtual environment (optional)

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install flask opencv-python face-recognition numpy pandas openpyxl
```

---

## Usage

### Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

---

### Capture Faces

1. Open the **Capture Face** page.
2. Enter student details.
3. Capture face images using the webcam.
4. Images are stored in the `dataset/` folder.

### Train Faces

1. Open the **Train Faces** page.
2. Train the captured images.
3. Encodings are stored in `trained_faces/`.

### Mark Attendance

1. Open the **Attendance** page.
2. Start face recognition.
3. Attendance is recorded automatically in `attendance.xlsx`.

---

## Privacy Notice

To protect privacy, the public repository does **not** include:

- Student face images (`dataset/`)
- Trained face encodings (`trained_faces/encodings.pkl`)
- Attendance records (`attendance.xlsx`)
- Student records (`students.xlsx`)

Users can generate these files themselves by capturing and training their own faces.

---

## Future Enhancements

- Database integration (MySQL/MongoDB)
- Admin login system
- Cloud storage support
- Attendance analytics dashboard
- Email notifications

---

## Author

**Y. Saranya**

Developed as a mini project using Flask, OpenCV, and Face Recognition for automated attendance management.

---

> **Note:** This project is not deployed online. GitHub Pages does not support Flask applications with OpenCV and Face Recognition. Please clone the repository and run the application locally to test all features.
