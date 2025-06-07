#!/usr/bin/env python3
import socket
import time
import random
import json
import os

# Load config
cfg_path = os.path.join(os.path.dirname(__file__), "../config/config.json")
with open(cfg_path) as f:
    cfg = json.load(f)

UDP_IP = cfg["udp"]["ip"]
PORT_MIN, PORT_MAX = cfg["udp"]["port_range"]
keywords = cfg["keywords"]
SLEEP_MIN, SLEEP_MAX = cfg["sleep_interval"]

def random_coord():
    lat = round(random.uniform(17.0, 18.0), 4)
    lon = round(random.uniform(77.5, 78.5), 4)
    return f"{lat}N {lon}E"

print("📡 Node A Active: Broadcasting Tactical Messages on random ports...\n")

while True:
    # pick a random port each iteration
    UDP_PORT = random.randint(PORT_MIN, PORT_MAX)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    keyword = random.choice(keywords)
    coord = random_coord()
    message = f"NODE_A: {keyword} at GRID {coord}"
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    print(f"[Sent → {UDP_IP}:{UDP_PORT}] {message}")
    sock.close()

    time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

