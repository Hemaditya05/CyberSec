# defense.py
import socket
import threading
import os
import random
from geopy.distance import geodesic
from geopy import Point
from geopy.distance import distance as geopy_distance

# Shared state
USER_DEFINED_PATH = [
    (32.7266, 74.8570, "Jammu City"),
    (32.7550, 74.8731, "Sainik Colony"),
    (32.6772, 74.8211, "Bari Brahmana"),
    (32.9000, 75.2000, "Tikri"),
    (33.0500, 75.3500, "Reasi"),
    (33.4100, 75.5200, "Banihal End"),
]
PATH_LOCK = threading.Lock()
history = []
socketio = None
stop_event = threading.Event()
mute_red_sound = [False]
DISTANCE_THRESHOLD_M = 500

def set_socketio(sio):
    global socketio
    socketio = sio

def set_stop_event(ev):
    global stop_event
    stop_event = ev

def get_user_path():
    with PATH_LOCK:
        return list(USER_DEFINED_PATH)

def add_path_point(lat, lon, label=None):
    with PATH_LOCK:
        USER_DEFINED_PATH.append((lat, lon, label or f"Point {len(USER_DEFINED_PATH)+1}"))

def reset_user_path():
    global USER_DEFINED_PATH
    with PATH_LOCK:
        USER_DEFINED_PATH = [
            (32.7266, 74.8570, "Jammu City"),
            (32.7550, 74.8731, "Sainik Colony"),
            (32.6772, 74.8211, "Bari Brahmana"),
            (32.9000, 75.2000, "Tikri"),
            (33.0500, 75.3500, "Reasi"),
            (33.4100, 75.5200, "Banihal End"),
        ]

def log_event(lat, lon, ts, status, details=""):
    try:
        with open("gps_log.txt", "a") as f:
            f.write(f"{ts},{lat},{lon},{status},{details}\n")
    except Exception as e:
        print(f"❌ Error logging event: {e}")

def nearest_path_distance(lat, lon):
    min_dist = float("inf")
    with PATH_LOCK:
        for plat, plon, _ in USER_DEFINED_PATH:
            d = geodesic((lat, lon), (plat, plon)).meters
            if d < min_dist:
                min_dist = d
    return min_dist

def generate_enemy_spoof(lat, lon):
    # Pick a random segment in USER_DEFINED_PATH and offset perpendicularly by 600–1000 m
    with PATH_LOCK:
        idx = random.randint(0, len(USER_DEFINED_PATH)-2)
        a = USER_DEFINED_PATH[idx]
        b = USER_DEFINED_PATH[idx+1]
    # Compute bearing from a->b
    point_a = Point(a[0], a[1])
    point_b = Point(b[0], b[1])
    base_bearing = geopy_distance(point_a, point_b).destination(point=point_a, bearing=90)
    # Choose a random perpendicular direction ±90°
    perp_bearing = (random.choice([90, -90]) + 0) % 360
    # Distance between 600 and 1000 meters
    d_m = random.uniform(600, 1000)
    spoof_point = geopy_distance(meters=d_m).destination(point=point_a, bearing=perp_bearing)
    return spoof_point.latitude, spoof_point.longitude

def start_defense_server():
    try:
        if os.path.exists("gps_log.txt"):
            os.remove("gps_log.txt")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 9999))
        server.listen(1)
        print("🛡️ Defense system online. Listening for GPS stream...")
        client, _ = server.accept()
        print("✅ Connected to GPS stream.")
        buffer = b""
        while not stop_event.is_set():
            chunk = client.recv(1024)
            if not chunk:
                print("❌ Client closed connection.")
                break
            buffer += chunk
            while b'\n' in buffer:
                message, buffer = buffer.split(b'\n', 1)
                data = message.decode().strip()
                if not data:
                    continue
                parts = data.split(',')
                if len(parts) < 3:
                    print("❌ Invalid data format.")
                    continue
                try:
                    lat, lon = float(parts[0]), float(parts[1])
                    ts = parts[2]
                except Exception as e:
                    print(f"❌ Invalid data: {e}")
                    continue
                # Primary 500 m detection
                path_dist = nearest_path_distance(lat, lon)
                status = "PATH" if path_dist <= DISTANCE_THRESHOLD_M else "SPOOF"
                details = f"Distance from path: {path_dist:.1f} m"
                # Emit sound if spoof
                if status == "SPOOF" and socketio and not mute_red_sound[0]:
                    socketio.emit('play_red_sound', {})
                # Save to history
                entry = [lat, lon, ts, status, details]
                history.append(entry)
                if len(history) > 50:
                    history.pop(0)
                log_event(lat, lon, ts, status, details)
                # Broadcast updates
                if socketio:
                    socketio.emit('history_update', {'history': history[-50:]})
        print("🛑 Defense system stopped.")
    except Exception as e:
        print(f"❌ Error in defense server: {e}")
    finally:
        client.close()
        server.close()

def toggle_mute_red_sound():
    try:
        mute_red_sound[0] = not mute_red_sound[0]
        if socketio:
            socketio.emit('mute_status', {'muted': mute_red_sound[0]})
    except Exception as e:
        print(f"❌ Error toggling mute: {e}")
