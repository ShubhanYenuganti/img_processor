# Image Processor

This tool processes a video file (`input/video.mp4`) by converting it into image frames, detecting objects using AWS Rekognition, and marking them with bounding boxes.

## Splitting Video
`split.py` uses OpenCV to extract every 30th frame (by default) from the video and saves them as JPG images in a folder.

## Labeling Frames
`detect.py` uses AWS Rekognition to analyze each saved frame, identifying objects and storing their labels, confidence scores, and bounding box coordinates in a `labels` directory.

## Marking Images
`detect.py` then uses the label data to create new images with drawn bounding boxes and captions that describe each detected object along with its confidence score.
