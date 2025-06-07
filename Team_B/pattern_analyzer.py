from collections import Counter
import re

LOGFILE = "intercepted/log.txt"

print("🧠 Analyzing intercepted battlefield traffic...\n")

try:
    with open(LOGFILE, "r") as f:
        logs = f.readlines()
except FileNotFoundError:
    print("❌ Log file not found.")
    exit()

# Extract node sources and messages
node_ids = []
messages = []

for line in logs:
    # Extract node name
    match_node = re.search(r'NODE_[A-Z]', line)
    if match_node:
        node_ids.append(match_node.group())

    # Extract full message payload
    msg = line.split("→")[-1].strip()
    messages.append(msg)

# Frequency analysis
node_count = Counter(node_ids)
msg_count = Counter(messages)

print("📡 Message Frequency by Node:")
for node, count in node_count.items():
    print(f"  - {node}: {count} packets")

print("\n🎯 Most Repeated Commands:")
for msg, count in msg_count.most_common(5):
    print(f"  - \"{msg}\" → {count} times")

# Detect suspicious spammy patterns
print("\n🔍 Potential Spam or Injection Candidates:")
for msg, count in msg_count.items():
    if count > 20:
        print(f"  ⚠️ \"{msg}\" appears {count} times — possible fake/loop flood")

