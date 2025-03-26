from dotenv import load_dotenv
from split import extract_frames
import os
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

if __name__ == "__main__": 
    video_path = "input/video.mp4"
    frame_dir = "frames"

    # Extract frames
    extract_frames(video_path, frame_dir)
