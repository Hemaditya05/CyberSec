# 🛰️ Smart Soldier LoRa Mesh: Sniffer Simulation (Enemy Interception Role)

This project simulates a battlefield LoRa mesh communication system using Python and standard networking tools. It focuses on the role of an enemy SIGINT (Signals Intelligence) operator — a passive eavesdropper listening to soldier-to-soldier LoRa-style communications, intercepting and analyzing critical messages without hardware.

---

## 🎯 Project Objective

Simulate a real-world scenario where:
- Soldiers (Node A, B, etc.) send LoRa-style messages containing tactical alerts and GPS data.
- A stealthy enemy node (Node C) intercepts those messages.
- Data is logged, analyzed, replayed, and summarized into threat intelligence reports.

---

## 🧠 Components

### 1. `node_a_sender.py`
- Simulates a soldier’s LoRa radio
- Broadcasts alerts like:  
  `NODE_A: ENEMY_SPOTTED at GRID 17.43N 78.43E`

### 2. `node_c_sniffer.py`
- Passive interceptor (you)
- Logs messages to `log.txt`
- Detects keywords (`ENEMY_SPOTTED`, etc.)
- Plays alert beeps
- Extracts and stores GPS coordinates to `geo_log.csv`

### 3. `generate_report.py`
- Parses intercepted data
- Builds `report.md` showing:
  - Total packets
  - Keyword frequency
  - GPS coordinates
  - References to `.pcapng` logs

### 4. `playback.py`
- Replays `log.txt` like a live enemy radio log feed

### 5. `pattern_analyzer.py`
- Analyzes:
  - Most frequent messages
  - Node activity levels
  - Potential fake/injection messages

### 6. `.pcapng` Logs
- Generated using `tcpdump`
- Viewable in Wireshark with filter:
  ```udp.port == 1337```

---

## 📂 Folder Structure

DLDR/Team_B/
├── intercepted/
│ ├── log.txt
│ └── geo_log.csv
├── logs/
│ └── mission_capture_*.pcapng
├── nodes/
│ ├── node_a_sender.py
│ └── node_c_sniffer.py
├── generate_report.py
├── playback.py
├── pattern_analyzer.py
├── report.md
└── README.md

yaml
Copy
Edit

---

## 🚀 How to Run

### Start Sender:
```bash
python3 nodes/node_a_sender.py
Start Sniffer:
bash
Copy
Edit
python3 nodes/node_c_sniffer.py
Capture Packets:
bash
Copy
Edit
sudo tcpdump -i lo udp port 1337 -w logs/mission_capture_$(date +%H%M).pcapng
Analyze + Report:
bash
Copy
Edit
python3 generate_report.py
python3 pattern_analyzer.py
Replay Logs:
bash
Copy
Edit
python3 playback.py intercepted/log.txt
⚠️ Disclaimer
This simulation does not use actual LoRa hardware. It is designed for educational and research purposes only — to help students and cyber professionals understand wireless mesh communication, passive interception, and data intelligence workflows in a fully controlled environment.

🧠 Role: You are the enemy signal interceptor.
📡 Mission: Detect, decode, and dominate.

vbnet
Copy
Edit

✅ Save and exit (`Ctrl + O`, `Enter`, `Ctrl + X`).
