import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import os
import time
import pandas as pd

TRAINED_PATH = "trained_faces/encodings.pkl"
STUDENTS_FILE = "students.xlsx"
ATTENDANCE_FILE = "attendance.xlsx"

# Track last attendance marking to avoid spamming entries
last_marked = {}

def _load_known():
    """Load face encodings and names from file."""
    if not os.path.exists(TRAINED_PATH):
        print("❌ Encodings file not found. Run training first.")
        return None, None
    with open(TRAINED_PATH, "rb") as f:
        known_encodings, known_names = pickle.load(f)
    if not known_encodings:
        print("❌ No encodings found in file.")
        return None, None
    return known_encodings, known_names

def _ensure_students_file(known_names):
    """Ensure students.xlsx exists or rebuild it from known faces."""
    if os.path.exists(STUDENTS_FILE):
        return

    students = []
    for combo in known_names:
        if "_" in combo:
            roll, name = combo.split("_", 1)
        else:
            roll, name = "", combo
        students.append({"Name": name, "Roll": roll})

    df = pd.DataFrame(students)
    df.to_excel(STUDENTS_FILE, index=False)
    print(f"✅ Created {STUDENTS_FILE} automatically from trained faces.")

def _mark_attendance(present_rolls):
    """Mark Present/Absent in attendance.xlsx for all students."""
    if not os.path.exists(STUDENTS_FILE):
        print("❌ students.xlsx missing. Please retrain first.")
        return

    students = pd.read_excel(STUDENTS_FILE)
    now = datetime.now()
    now_date = now.strftime("%Y-%m-%d")
    now_time = now.strftime("%H:%M:%S")



    # Build today's attendance list
    records = []
    for _, row in students.iterrows():
        status = "Present" if str(row["Roll"]) in present_rolls else "Absent"
        records.append({
            "Name": row["Name"],
            "Roll": row["Roll"],
            "Date": now_date,
            "Time": now_time,
            "Status": status
        })

    new_df = pd.DataFrame(records)

    # If attendance file exists, merge intelligently
    if os.path.exists(ATTENDANCE_FILE):
        old_df = pd.read_excel(ATTENDANCE_FILE)
        combined = pd.concat([old_df, new_df], ignore_index=True)

        #Remove duplicates per day per roll
        combined["Date"] = pd.to_datetime(combined["Date"] + " " + combined["Time"])
        combined.drop_duplicates(subset=["Roll", "Date"], keep="last", inplace=True)
    else:
        combined = new_df

    #Save with better formatting
    with pd.ExcelWriter(ATTENDANCE_FILE, engine="openpyxl") as writer:
        combined.to_excel(writer, index=False, sheet_name="Attendance")
        worksheet = writer.sheets["Attendance"]

        # Auto column width
        for column_cells in worksheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    print(f"✅ Attendance updated for {now_date}. File: {ATTENDANCE_FILE}")

def take_attendance(threshold=0.45):
    """Perform live face recognition and mark attendance."""
    known_encodings, known_names = _load_known()
    if known_encodings is None:
        return

    _ensure_students_file(known_names)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ ERROR: Cannot open webcam.")
        return

    print("🎥 Attendance started. Press 'q' to quit.")
    present_rolls = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for faster processing
        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare against known encodings
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(distances) == 0:
                continue

            best_index = int(np.argmin(distances))
            best_distance = float(distances[best_index])

            if best_distance <= threshold:
                name_combo = known_names[best_index]
                if "_" in name_combo:
                    roll, name = name_combo.split("_", 1)
                else:
                    roll, name = "", name_combo

                present_rolls.add(str(roll))

                top, right, bottom, left = [v * 4 for v in face_location]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} ({roll}) {best_distance:.2f}", (left, top - 10),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                # Draw red box for unknown
                top, right, bottom, left = [v * 4 for v in face_location]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Smart Face Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save attendance when webcam closes
    _mark_attendance(present_rolls)
    print("📝 Attendance process completed.")
