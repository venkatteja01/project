import cv2
import os
import subprocess
from ultralytics import YOLO

# Load trained pothole model
model = YOLO("pothole_model.pt")

# Stream key
STREAM_KEY = os.getenv("YT_STREAM_KEY")
YOUTUBE_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# Camera
cap = cv2.VideoCapture(0)
WIDTH, HEIGHT = 640, 480
FPS = 15

# FFmpeg process
ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "veryfast",
    "-f", "flv",
    YOUTUBE_URL
]

process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    results = model(frame, conf=0.4)

    pothole_count = 0

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label in ["pothole", "crack"]:
                pothole_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.putText(frame, f"Defects: {pothole_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    process.stdin.write(frame.tobytes())

cap.release()
process.stdin.close()
process.wait()
