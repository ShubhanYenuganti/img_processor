import cv2
import os

def extract_frames(path, output_dir, interval = 30): 
    cap = cv2.VideoCapture(path)
    frame_count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            cv2.imwrite(f"{output_dir}/frame_{saved_count}.jpg", frame)
            saved_count += 1
        
        frame_count += 1
        
    cap.release()

    print(f"Extracted {saved_count} frames")