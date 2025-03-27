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
                                             MaxLabels = 10,
                                             MinConfidence = 65,
                                            )
    return response['Labels']

def annotate_img(img_path, labels):
    image = cv2.imread(img_path)
    H, W, _ = image.shape

    for label in labels:
        name = label['Name']
        for instance in label.get("Instances", []):
            if "BoundingBox" in instance:
                box = instance["BoundingBox"]
                x1 = int(box['Left'] * W)
                y1 = int(box['Top'] * H)
                width = int(box['Width'] * W)
                height = int(box['Height'] * H)

                cv2.rectangle(image, (x1, y1), (x1 + width, y1 + height), (0, 255, 0), 3)
                caption = f"{name} with {int(instance['Confidence'])} %"
                cv2.putText(image, caption, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 2)

    return image

if __name__ == "__main__": 
    video_path = "input/video.mp4"
    frame_dir = "frames"
    labels_dir = "labels"
    annotations_dir = "annotations"

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

            annotated = annotate_img(img_path, labels)
            annotated_path = os.path.join(annotations_dir, file.replace(".jpg", "_annotated.jpg"))
            cv2.imwrite(annotated_path, annotated)
            print(f"Processed {file} with labels and annotations.")