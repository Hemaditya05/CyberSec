from collections import Counter
import re
from datetime import datetime

LOGFILE = "intercepted/log.txt"
GEOLOG = "intercepted/geo_log.csv"
REPORT = "report.md"

with open(LOGFILE, "r") as f:
    logs = f.readlines()

total_packets = len(logs)
keywords = ["ENEMY_SPOTTED", "MEDIC_REQUEST", "RETREAT", "NODE"]
hits = Counter()

for line in logs:
    for word in keywords:
        if word in line:
            hits[word] += 1

# Extract coordinates
coords = []
try:
    with open(GEOLOG, "r") as g:
        for row in g:
            match = re.findall(r"\d+\.\d+", row)
            if len(match) >= 2:
                coords.append((match[0], match[1]))
except:
    pass

# Generate Markdown
with open(REPORT, "w") as r:
    r.write(f"# 🛰️ LoRa Intercept Report\n")
    r.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    r.write("## 🎯 Summary\n")
    r.write(f"- Total Packets: {total_packets}\n")
    r.write(f"- Keywords:\n")
    for k, v in hits.items():
        r.write(f"  - {k}: {v}\n")
    r.write("\n## 📍 Coordinates Captured\n")
    for lat, lon in coords:
        r.write(f"- {lat}, {lon}\n")
    r.write("\n## 📂 Log File Reference\n")
    r.write("- intercepted/log.txt\n")
    r.write("- intercepted/geo_log.csv\n")
    r.write("- logs/mission_capture_*.pcapng\n")
