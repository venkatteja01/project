import time
import Adafruit_DHT
import serial

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

gps = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

def read_gps():
    try:
        line = gps.readline().decode(errors="ignore")
        if "$GPGGA" in line:
            parts = line.split(",")
            return parts[2], parts[4]
    except:
        pass
    return None, None

def read_lidar():
    return 1.2  # placeholder

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    lat, lon = read_gps()
    lidar = read_lidar()

    print({
        "temp": temperature,
        "humidity": humidity,
        "lat": lat,
        "lon": lon,
        "lidar": lidar
    })

    time.sleep(5)
