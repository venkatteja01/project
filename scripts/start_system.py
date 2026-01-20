import subprocess
import time

print("Starting sensors...")
sensor = subprocess.Popen(["python3", "sensor_reader.py"])

time.sleep(2)

print("Starting YOLO livestream...")
stream = subprocess.Popen(["python3", "yolo_pothole_stream.py"])

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping system...")
    sensor.terminate()
    stream.terminate()
