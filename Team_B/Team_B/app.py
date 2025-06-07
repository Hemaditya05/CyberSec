# app.py
#!/usr/bin/env python3
import os
import json
import signal
import subprocess
from flask import Flask, render_template, request, redirect, url_for, Response, jsonify

app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend/static"
)

BASE_DIR         = os.path.dirname(__file__)
CONFIG_PATH      = os.path.join(BASE_DIR, "config/config.json")
LOG_FILE_PATH    = os.path.join(BASE_DIR, "intercepted/log.txt")
GEO_LOG_PATH     = os.path.join(BASE_DIR, "intercepted/geo_log.csv")
ACTIVE_PORT_PATH = os.path.join(BASE_DIR, "intercepted/active_port.txt")

A_PROCESS = None
C_PROCESS = None

def read_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def write_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    cfg = read_config()
    if request.method == "POST":
        port_min = int(request.form["port_min"])
        port_max = int(request.form["port_max"])
        keywords = request.form["keywords"].split(",")
        sleep_min = float(request.form["sleep_min"])
        sleep_max = float(request.form["sleep_max"])
        cfg["udp"]["port_range"] = [port_min, port_max]
        cfg["keywords"] = [k.strip() for k in keywords if k.strip()]
        cfg["sleep_interval"] = [sleep_min, sleep_max]
        write_config(cfg)
        return redirect(url_for("index"))
    return render_template("index.html", cfg=cfg)

@app.route("/start_a")
def start_a():
    global A_PROCESS
    if A_PROCESS:
        try:
            os.kill(A_PROCESS.pid, signal.SIGTERM)
        except:
            pass
    cmd = ["python3", "nodes/node_a_sender.py"]
    A_PROCESS = subprocess.Popen(cmd, cwd=BASE_DIR)
    return redirect(url_for("index"))

@app.route("/start_c")
def start_c():
    global C_PROCESS
    if C_PROCESS:
        try:
            os.kill(C_PROCESS.pid, signal.SIGTERM)
        except:
            pass
    cmd = ["python3", "nodes/node_c_sniffer.py"]
    C_PROCESS = subprocess.Popen(cmd, cwd=BASE_DIR)
    return redirect(url_for("index"))

@app.route("/stop_all")
def stop_all():
    global A_PROCESS, C_PROCESS
    for proc in (A_PROCESS, C_PROCESS):
        if proc:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except:
                pass
    A_PROCESS = C_PROCESS = None
    return redirect(url_for("index"))

@app.route("/get_logs")
def get_logs():
    if not os.path.isfile(LOG_FILE_PATH):
        return Response("", mimetype="text/plain")
    with open(LOG_FILE_PATH, "r") as f:
        all_lines = f.readlines()
    return Response("".join(all_lines[-200:]), mimetype="text/plain")

@app.route("/get_active_port")
def get_active_port():
    if not os.path.isfile(ACTIVE_PORT_PATH):
        return Response("", mimetype="text/plain")
    with open(ACTIVE_PORT_PATH, "r") as f:
        port = f.read().strip()
    return Response(port, mimetype="text/plain")

@app.route("/get_geo_logs")
def get_geo_logs():
    data = []
    if os.path.isfile(GEO_LOG_PATH):
        with open(GEO_LOG_PATH, "r") as f:
            for line in f:
                ts, lat, lng = line.strip().split(",")
                data.append({"time": ts, "lat": float(lat), "lng": float(lng)})
    return jsonify(data)

@app.route("/run_pattern")
def run_pattern():
    proc = subprocess.Popen(
        ["python3", "pattern_analyzer.py"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    output, _ = proc.communicate()
    return Response(output or "No output from Pattern Analyzer.", mimetype="text/plain")

@app.route("/run_report")
def run_report():
    proc = subprocess.Popen(
        ["python3", "generate_report.py"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    output, _ = proc.communicate()
    return Response(output or "No output from Generate Report.", mimetype="text/plain")

@app.route("/run_playback")
def run_playback():
    proc = subprocess.Popen(
        ["python3", "playback.py"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    output, _ = proc.communicate()
    return Response(output or "No output from Playback.", mimetype="text/plain")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

