from dotenv import load_dotenv
from split import extract_frames
import boto3
import json
import cv2
import os
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

reko_client = boto3.client('rekognition',
                           aws_access_key_id = AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def detect_labels(img_path):
    with open(img_path, 'rb') as img:
        image_bytes = img.read()
        response = reko_client.detect_labels(Image={'Bytes': image_bytes},
                                            minConfidence = 65,
                                            Attributes = ['ALL']
                                            )
    return response['labels']

if __name__ == "__main__": 
    video_path = "input/video.mp4"
    frame_dir = "frames"
    labels_dir = "labels"

    # Extract frames
    extract_frames(video_path, frame_dir)

    # Detect all labels in each frame 
    for file in os.listdir(frame_dir):
        if file.endswith(".jpg"):
            img_path = os.path.join(frame_dir, file)

            labels = detect_labels(img_path)

            labels_file = os.path.join(labels_dir, file.replace(".jpg", ".json"))
            with open(labels_file, 'w') as f:
                json.dump(labels, f, indent=2)