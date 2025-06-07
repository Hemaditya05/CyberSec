 # CyberSec

**CyberSec** is a cybersecurity simulation suite that showcases advanced surveillance and deception detection mechanisms across two core projects:

* **Team A – GPS Spoofing Detection System**
* **Team B – LoRa Mesh Network Interception and Analysis**

This repository is structured to provide realistic defense simulations aligned with border-security scenarios, combining signal integrity monitoring, real-time geographic intelligence, and adaptive analysis of unauthorized transmissions.

---

## Projects Overview

### Team A – GPS Spoofing Detection System

A real-time monitoring and defense system that identifies GPS spoofing attempts by simulating a drone's path near high-security borders. The system tracks legitimate vs. spoofed coordinates based on:

* Geolocation thresholds
* Speed deviation checks
* Terrain height analysis
* Blackout and reflection zones
* Weather-adjusted path drift tolerance

**Features:**

* Socket-based real-time GPS stream receiver
* Interactive map visualization using Folium
* Alert logging and sound feedback on spoof detection
* Frontend control dashboard (Flask + Socket.IO)

### Team B – LoRa Mesh Interception & Signal Replay

A passive surveillance and analysis tool simulating smart soldier communication interception. This project detects tactical keywords in simulated LoRa mesh messages transmitted over UDP.

**Components:**

* **Node A:** Broadcasts random encrypted messages with grid coordinates.
* **Node C:** Sniffs UDP traffic, detects keywords, logs active ports and geographic metadata.
* **Playback & Analysis:** Includes real-time replay, report generation, and keyword-based pattern analysis.

**Features:**

* Dynamic port scanning and discovery
* Sniffer dashboard for visual log analysis and map tracing
* Pattern detection and anomaly frequency visualization

---

## Folder Structure

```
CyberSec/
├── Team_A/                  # GPS Spoofing Defense System
│   ├── gps_stream_simulator.py
│   ├── gps_defense_realtime.py
│   ├── templates/
│   ├── static/
│   ├── app.py               # Web dashboard
│   └── logs/
│
├── Team_B/                  # LoRa Signal Sniffer & Analyzer
│   ├── nodes/
│   │   ├── node_a_sender.py
│   │   └── node_c_sniffer.py
│   ├── intercepted/
│   ├── generate_report.py
│   ├── pattern_analyzer.py
│   ├── playback.py
│   ├── config/
│   │   └── config.json
│   └── app.py               # Web interface and control
```

---

## Requirements

* Python 3.9+
* Flask
* Folium
* Geopy
* Scapy
* Chart.js (frontend)
* Leaflet.js (frontend)
* Linux or Windows (Kali Linux preferred for Team B)

To install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage Instructions

Each project includes an individual `app.py` that can be executed independently to launch the full simulation and frontend interface. Detailed guides are provided in the respective folders.

---

## License

This repository is licensed for academic and research purposes. Unauthorized misuse or deployment in real-world surveillance or malicious contexts is prohibited.


