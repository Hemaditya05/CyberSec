import time
import os

LOGFILE = "intercepted/log.txt"

if not os.path.exists(LOGFILE):
    print("No intercepted log found.")
    exit()

print("🔁 Replaying LoRa traffic feed...\n")

with open(LOGFILE, "r") as f:
    lines = f.readlines()

for line in lines:
    print(line.strip())
    time.sleep(0.8)  # delay between messages to simulate live radio feed
