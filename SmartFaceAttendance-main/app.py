from flask import Flask, render_template, request, redirect, url_for, flash
import os
import threading
from capture_face import capture_images
from train_faces import train_model
from attendance_face import take_attendance
from flask import send_file
import pandas as pd

app = Flask(__name__)
app.secret_key = "change_this_secret"  # required for flash messages

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Capture Student Images
@app.route('/capture', methods=['GET', 'POST'])
def capture():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        roll = request.form.get('roll', '').strip()
        if not name or not roll:
            flash("Name and Roll Number are required!", "error")
            return redirect(url_for('capture'))

        # Run capture in background thread
        t = threading.Thread(target=capture_images, args=(name, roll), daemon=True)
        t.start()
        flash(f"Started capturing for {name} ({roll}). Use camera window: 'c' = capture, 'q' = quit.", "info")
        return redirect(url_for('index'))

    return render_template('capture.html')

# Train Faces
@app.route('/train')
def train():
    try:
        train_model()
        flash("Training completed successfully!", "success")
    except Exception as e:
        flash(f"Training failed: {e}", "error")
    return render_template('train.html')

# Take Attendance
@app.route('/attendance')
def attendance():
    t = threading.Thread(target=take_attendance, daemon=True)
    t.start()
    flash("Attendance started. Webcam window will open. Press 'q' to quit.", "info")
    return render_template('attendance.html')

# View Attendance Records
@app.route('/view_attendance')
def view_attendance():
    import pandas as pd
    records = []
    if os.path.exists("attendance.xlsx"):
        try:
            df = pd.read_excel("attendance.xlsx")
            records = df.to_dict(orient='records')
        except Exception:
            df = pd.read_csv("attendance.csv")
            records = df.to_dict(orient='records')
    elif os.path.exists("attendance.csv"):
        import csv
        with open("attendance.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = list(reader)
    return render_template('attendance_table.html', records=records)

@app.route('/clear_attendance')
def clear_attendance():
    path = "attendance.xlsx"
    if os.path.exists(path):
        # recreate empty dataframe with same columns
        df = pd.DataFrame(columns=["Name", "Roll", "Date", "Status"])
        df.to_excel(path, index=False)
    return redirect(url_for('view_attendance'))

@app.route('/open_attendance_sheet')
def open_attendance_sheet():
    """View Excel sheet in browser (not download)."""
    path = "attendance.xlsx"
    if not os.path.exists(path):
        flash("Attendance sheet not found!", "error")
        return redirect(url_for('view_attendance'))

    # Convert Excel content to an HTML table view
    df = pd.read_excel(path)
    table_html = df.to_html(classes="excel-view", index=False)
    return f"""
    <html>
    <head>
        <title>Attendance Excel View</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            .excel-view {{
                border-collapse: collapse;
                width: 100%;
            }}
            .excel-view th, .excel-view td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: center;
            }}
            .excel-view th {{
                background-color: #f0f0f0;
            }}
        </style>
    </head>
    <body>
        <h2>📘 Attendance Sheet</h2>
        {table_html}
        <br>
        <a href="/view_attendance" style="text-decoration:none; background:#007BFF; color:white; padding:10px 20px; border-radius:5px;">⬅ Back to Attendance List</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
