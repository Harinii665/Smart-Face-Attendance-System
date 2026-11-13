import cv2
import os

def capture_images(name, roll, save_count_target=15):
    folder = os.path.join("dataset", f"{roll}_{name}")
    os.makedirs(folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam for capturing images.")
        return

    count = len([f for f in os.listdir(folder) if f.lower().endswith(('.jpg','.jpeg','.png'))])
    print(f"Capture started for {name} ({roll}). Existing images: {count}. Press 'c' to capture, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: failed to read frame from webcam.")
            break

        cv2.putText(frame, f"{name} ({roll}) - Press c to capture ({count}/{save_count_target})",
                    (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.imshow("Capture Images - Press c to save, q to quit", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            filename = os.path.join(folder, f"{count}.jpg")
            cv2.imwrite(filename, frame)
            count += 1
            print(f"Saved: {filename}")
            if count >= save_count_target:
                print("Reached target count.")
                break
        elif key == ord('q'):
            print("Capture stopped by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Capture finished for {name} ({roll}). Total images: {count}")
