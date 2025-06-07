#!/usr/bin/env python3
# node_c_sniffer.py (modified)

import os
import socket
import datetime
import re
from scapy.all import sniff, UDP, IP

# Paths
BASE_DIR       = os.path.dirname(__file__)       # DLRL/Team_B/nodes
INTERCEPTED_DIR = os.path.join(BASE_DIR, "../intercepted")
LOGFILE        = os.path.join(INTERCEPTED_DIR, "log.txt")
GEOLOG         = os.path.join(INTERCEPTED_DIR, "geo_log.csv")
ACTIVE_PORT_FILE = os.path.join(INTERCEPTED_DIR, "active_port.txt")

# Ensure output directories/files exist
os.makedirs(INTERCEPTED_DIR, exist_ok=True)
for path in (LOGFILE, GEOLOG, ACTIVE_PORT_FILE):
    if not os.path.isfile(path):
        open(path, "w").close()

# If a stale active_port.txt exists, clear it on startup
with open(ACTIVE_PORT_FILE, "w") as f:
    f.write("")

# Keywords → emoji mapping
keywords = {
    "ENEMY_SPOTTED": "🔴 We are Discovered",
    "MEDIC_REQUEST": "🔵 Injury Detected",
    "RETREAT":       "🟡 RETREATING"
}

port_found = False  # Global flag so we only write the port once

def handle_pkt(pkt):
    global port_found

    if UDP in pkt and IP in pkt:
        data = bytes(pkt[UDP].payload)
        try:
            message = data.decode(errors="ignore")
        except:
            return

        now = datetime.datetime.now().strftime("%H:%M:%S")
        src_ip   = pkt[IP].src
        src_port = pkt[UDP].sport
        dst_port = pkt[UDP].dport

        # If we haven't discovered a port yet, write it now:
        if not port_found:
            port_found = True
            with open(ACTIVE_PORT_FILE, "w") as pf:
                pf.write(str(dst_port))
            print(f"⚡️ Port discovered: {dst_port}")

        # Log entry
        log_entry = f"[{now}] FROM {src_ip}:{src_port} → dst_port {dst_port} → {message}"
        print(log_entry)
        with open(LOGFILE, "a") as f:
            f.write(log_entry + "\n")

        # Check for keywords to trigger tone
        for k in keywords:
            if k in message:
                print(f"  ▶ {keywords[k]}")
                os.system('play -nq -t alsa synth 0.2 sine 880')

        # Extract GRID coords and append to CSV
        if "GRID" in message:
            coord_match = re.findall(r"(\d+\.\d+)[^\d]+(\d+\.\d+)", message)
            if coord_match:
                lat, lng = coord_match[0]
                with open(GEOLOG, "a") as geo:
                    geo.write(f"{now},{lat},{lng}\n")

print("🎧 Node C Sniffer online: sniffing all UDP packets...\n")
# Start sniffing on loopback (UDP only)
sniff(iface="lo", prn=handle_pkt, filter="udp", store=False)

