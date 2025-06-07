 // static/js/script.js
const socket = io();
let isEditingPath = false;

// Initialize Leaflet map without zoom on click
let map = L.map('map', {
    doubleClickZoom: false,
    zoomControl: false,
    scrollWheelZoom: false,
    dragging: true,
    tap: false
}).setView([32.7550, 74.8731], 8);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let pointsLayer = L.layerGroup().addTo(map);
let pathLayer = L.polyline([], { color: 'blue', weight: 2.5, opacity: 0.6 }).addTo(map);

socket.on('history_update', data => {
    pointsLayer.clearLayers();
    let lastPoint = null;
    data.history.forEach(point => {
        const [lat, lon, ts, status] = point;
        lastPoint = [lat, lon];
        let color = status === 'PATH' ? '#07ed66' : '#e94560';
        L.circleMarker([lat, lon], {
            radius: 8,
            color: color,
            fillColor: color,
            fillOpacity: 0.9,
            weight: 3
        }).addTo(pointsLayer);
        document.getElementById('log').innerHTML += `<div>${ts} - ${status}: (${lat.toFixed(4)}, ${lon.toFixed(4)})</div>`;
        document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight;
    });
    if (lastPoint) map.panTo(lastPoint, { animate: true, duration: 0.5 });
});

socket.on('path_update', data => {
    pathLayer.setLatLngs(data.path.map(p => [p[0], p[1]]));
    updatePathList();
});

socket.on('stream_status', data => {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    if (data.status === 'started') {
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } else if (data.status === 'stopped') {
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
});

socket.on('play_red_sound', () => {
    if (!window.redSoundMuted) {
        new Audio('https://www.soundjay.com/buttons/beep-01a.mp3').play();
    }
});

socket.on('mute_status', data => {
    window.redSoundMuted = data.muted;
    document.getElementById('muteBtn').textContent = data.muted ? "Unmute Red Sound" : "Mute Red Sound";
});

function updatePathList() {
    fetch('/api/path')
        .then(res => res.json())
        .then(path => {
            const pathList = document.getElementById('pathList');
            pathList.innerHTML = '';
            path.forEach((pt, idx) => {
                let li = document.createElement('li');
                li.className = "list-group-item";
                li.textContent = `${pt[2] || 'Point'}: ${pt[0].toFixed(4)}, ${pt[1].toFixed(4)}`;
                pathList.appendChild(li);
            });
        });
}
updatePathList();

map.on('click', function(e) {
    if (!isEditingPath) return;
    const label = document.getElementById('pointName').value || undefined;
    fetch('/api/path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat: e.latlng.lat, lon: e.latlng.lng, label })
    }).then(() => {
        updatePathList();
    });
});

document.getElementById('editPathBtn').onclick = function() {
    isEditingPath = !isEditingPath;
    this.classList.toggle('active', isEditingPath);
    document.getElementById('pointName').disabled = !isEditingPath;
    this.textContent = isEditingPath ? "Click on Map to Add" : "Edit Path";
};

document.getElementById('startBtn').onclick = () => socket.emit('start_stream');
document.getElementById('stopBtn').onclick = () => socket.emit('stop_stream');
document.getElementById('muteBtn').onclick = () => socket.emit('toggle_mute');
document.getElementById('clearPath').onclick = () => {
    fetch('/api/reset_path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    }).then(() => updatePathList());
};
