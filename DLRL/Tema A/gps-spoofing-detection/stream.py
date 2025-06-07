# stream.py
import socket
import threading
import time
import random
from datetime import datetime
from geopy import Point
from geopy.distance import geodesic, distance as geopy_distance

# Shared stop_event for both defense and stream
stop_event = threading.Event()

def set_stop_event(ev):
    global stop_event
    stop_event = ev

HOST, PORT = 'localhost', 9999
STREAM_INTERVAL = 2  # seconds between points

# Defined patrol path (exact coordinates)
USER_PATH = [
    (32.7266, 74.8570, "Jammu City"),
    (32.7550, 74.8731, "Sainik Colony"),
    (32.6772, 74.8211, "Bari Brahmana"),
    (32.9000, 75.2000, "Tikri"),
    (33.0500, 75.3500, "Reasi"),
    (33.4100, 75.5200, "Banihal End"),
]

# Counter to ensure initial points follow the path exactly
send_count = 0

def generate_random_green():
    """
    Pick a random segment along USER_PATH, choose a point between endpoints,
    then offset it by up to 50 meters to simulate slight GPS noise (always <500m).
    """
    idx = random.randint(0, len(USER_PATH) - 2)
    a_lat, a_lon, _ = USER_PATH[idx]
    b_lat, b_lon, _ = USER_PATH[idx + 1]
    frac = random.random()
    base_lat = a_lat + frac * (b_lat - a_lat)
    base_lon = a_lon + frac * (b_lon - a_lon)
    offset_m = random.uniform(0, 50)
    bearing = random.uniform(0, 360)
    base_point = Point(base_lat, base_lon)
    noisy = geopy_distance(meters=offset_m).destination(point=base_point, bearing=bearing)
    return noisy.latitude, noisy.longitude

def generate_random_red():
    """
    Pick a random segment’s start point and offset it by 600–1000 meters
    perpendicular to that segment to simulate an enemy jump far off-path.
    """
    idx = random.randint(0, len(USER_PATH) - 2)
    a_lat, a_lon, _ = USER_PATH[idx]
    b_lat, b_lon, _ = USER_PATH[idx + 1]
    # Approximate segment bearing (a→b), then perpendicular ±90°
    bearing_ab = geodesic(Point(a_lat, a_lon), Point(b_lat, b_lon)).initial
    perp_bearing = (bearing_ab + 90) % 360
    if random.choice([True, False]):
        perp_bearing = (perp_bearing + 180) % 360
    offset_m = random.uniform(600, 1000)
    base_point = Point(a_lat, a_lon)
    spoofed = geopy_distance(meters=offset_m).destination(point=base_point, bearing=perp_bearing)
    return spoofed.latitude, spoofed.longitude

def start_stream():
    global send_count
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"🚁 Connected to defense core at {HOST}:{PORT}")
        while not stop_event.is_set():
            # First send the exact USER_PATH points in order (no noise/spoof)
            if send_count < len(USER_PATH):
                lat, lon, _ = USER_PATH[send_count]
                send_count += 1
            else:
                # After initial path, 15% chance of spoof, else slight-noise green
                if random.random() < 0.15:
                    lat, lon = generate_random_red()
                else:
                    lat, lon = generate_random_green()
            ts = datetime.utcnow().isoformat() + 'Z'
            msg = f"{lat:.6f},{lon:.6f},{ts}\n"
            s.send(msg.encode())
            time.sleep(STREAM_INTERVAL)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        s.close()
