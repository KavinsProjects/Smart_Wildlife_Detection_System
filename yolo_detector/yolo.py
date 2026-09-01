import os
import cv2
import numpy as np
import yt_dlp as youtube_dl
from ultralytics import YOLO

# Define the path to the YOLO model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "best.pt")

# Load the YOLO model once to optimize performance
model = YOLO(MODEL_PATH)
print("✅ YOLO model loaded successfully!")

# Define class names for detection
ANIMAL_CLASSES = [ "elephant","wildboar"]

def get_stream_url(youtube_url: str):
    """
    Extracts the best available streamable video URL from a YouTube link.
    """
    try:
        ydl_opts = {
            "format": "best[ext=mp4]",
            "quiet": True,
            "noplaylist": True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict.get("url")
    except Exception as e:
        print(f"❌ Error retrieving stream URL: {e}")
        return None

def detect_animal_in_frame(frame):
    """
    Runs YOLO detection on a single frame and returns detected objects.
    """
    if frame is None:
        return []

    results = model(frame, verbose=False)
    detected_objects = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = round(float(box.conf[0]), 2)
            cls = int(box.cls[0])

            if 0 <= cls < len(ANIMAL_CLASSES):
                detected_objects.append({
                    "class": ANIMAL_CLASSES[cls],
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2)
                })

    return detected_objects

def process_stream(youtube_url):
    """
    Streams the video from YouTube, extracts frames, and detects animals.
    Prints the mean detection results per second in the terminal.
    """
    stream_url = get_stream_url(youtube_url)
    if not stream_url:
        raise Exception("❌ Unable to retrieve stream URL")

    print(f"🎥 Streaming video from: {stream_url}")

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise Exception("❌ Error: Unable to open video stream!")

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps <= 0:
        video_fps = 30  # Default to 30 FPS if metadata is missing

    frame_interval = max(1, int(video_fps / 30))  # Process 30 FPS
    duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / video_fps)  # Video duration in seconds

    print(f"📊 Video FPS: {video_fps}, Duration: {duration:.2f} seconds")

    for sec in range(int(duration)):
        detections_per_second = {}

        for frame_num in range(5):  # Process 30 frames per second
            frame_index = sec * int(video_fps) + frame_num * frame_interval
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

            success, frame = cap.read()
            if not success or frame is None:
                print(f"⚠️ Skipping frame {frame_index} (empty or corrupt)")
                continue

            detected_objects = detect_animal_in_frame(frame)

            for obj in detected_objects:
                class_name = obj["class"]
                confidence = obj["confidence"]

                if class_name not in detections_per_second:
                    detections_per_second[class_name] = {"total_conf": 0.0, "count": 0}

                detections_per_second[class_name]["total_conf"] += confidence
                detections_per_second[class_name]["count"] += 1

        # Calculate mean confidence for each class in the current second
        final_detections = [
            {
                "class": class_name,
                "mean_confidence": round(data["total_conf"] / data["count"], 2)
            }
            for class_name, data in detections_per_second.items()
            if data["count"] > 0
        ]

        # Print results for the current second
        print(f"⏱️ Second {sec + 1}:")
        for detection in final_detections:
            print(f"  - {detection['class']}: Mean Confidence = {detection['mean_confidence']}")

    cap.release()
    print("✅ Video processing complete.")