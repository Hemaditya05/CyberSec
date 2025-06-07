# app.py
import threading
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from defense import (
    start_defense_server, set_socketio as set_defense_socketio,
    set_stop_event as set_defense_stop_event, add_path_point, get_user_path,
    toggle_mute_red_sound
)
from stream import start_stream, set_stop_event as set_stream_stop_event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

stop_event = threading.Event()
set_defense_stop_event(stop_event)
set_stream_stop_event(stop_event)
set_defense_socketio(socketio)

server_thread = None
stream_thread = None
is_running = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/path', methods=['GET'])
def get_path():
    return jsonify(get_user_path())

@app.route('/api/path', methods=['POST'])
def post_path():
    data = request.json
    lat = float(data['lat'])
    lon = float(data['lon'])
    label = data.get('label', None)
    add_path_point(lat, lon, label)
    socketio.emit('path_update', {'path': get_user_path()})
    return jsonify({"ok": True})

@app.route('/api/reset_path', methods=['POST'])
def reset_path():
    from defense import reset_user_path
    reset_user_path()
    socketio.emit('path_update', {'path': get_user_path()})
    return jsonify({"ok": True})

@socketio.on('connect')
def handle_connect():
    socketio.emit('stream_status', {'status': 'stopped' if not is_running else 'started'})
    socketio.emit('path_update', {'path': get_user_path()})

@socketio.on('start_stream')
def handle_start_stream():
    global server_thread, stream_thread, is_running
    if not is_running:
        is_running = True
        stop_event.clear()
        server_thread = threading.Thread(target=start_defense_server, daemon=True)
        stream_thread = threading.Thread(target=start_stream, daemon=True)
        server_thread.start()
        stream_thread.start()
        socketio.emit('stream_status', {'status': 'started'})
    else:
        socketio.emit('stream_status', {'status': 'error', 'message': 'Stream already active'})

@socketio.on('stop_stream')
def handle_stop_stream():
    global is_running
    is_running = False
    stop_event.set()
    socketio.emit('stream_status', {'status': 'stopped'})

@socketio.on('toggle_mute')
def handle_toggle_mute():
    toggle_mute_red_sound()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
