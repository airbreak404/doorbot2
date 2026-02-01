from flask import Flask, jsonify, render_template_string, request
from datetime import datetime
from threading import Timer

app = Flask(__name__)

# State management
door_state = {
    "letmein": False,
    "last_command_time": None,
    "last_unlock_user": None
}

# Simple web interface HTML
WEB_INTERFACE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Doorbot Control Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .button {
            display: inline-block;
            padding: 15px 30px;
            margin: 10px 5px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .unlock-btn {
            background: #4CAF50;
            color: white;
        }
        .unlock-btn:hover {
            background: #45a049;
        }
        .lock-btn {
            background: #f44336;
            color: white;
        }
        .lock-btn:hover {
            background: #da190b;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            background: #e3f2fd;
        }
        .locked { background: #ffebee; }
        .unlocked { background: #e8f5e9; }
        .log {
            margin-top: 20px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
            max-height: 200px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚪 Doorbot Control Panel</h1>
        <div>
            <button class="button unlock-btn" onclick="unlockDoor()">Unlock Door</button>
            <button class="button lock-btn" onclick="lockDoor()">Reset Lock State</button>
        </div>
        <div id="status" class="status">
            <strong>Status:</strong> <span id="statusText">Locked</span><br>
            <strong>Last command:</strong> <span id="lastCommand">None</span><br>
            <strong>Server:</strong> newyakko.cs.wmich.edu
        </div>
        <div class="log">
            <strong>Activity Log:</strong>
            <div id="activityLog">No activity yet</div>
        </div>
    </div>
    <script>
        let logEntries = [];

        function addLogEntry(message) {
            const timestamp = new Date().toLocaleTimeString();
            logEntries.unshift(`[${timestamp}] ${message}`);
            if (logEntries.length > 10) logEntries.pop();
            document.getElementById('activityLog').innerHTML = logEntries.join('<br>');
        }

        function unlockDoor() {
            fetch('/unlock', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    updateStatus();
                    addLogEntry('✅ Unlock command sent');
                    alert('Unlock command sent! Door will unlock on next client poll.');
                })
                .catch(err => {
                    addLogEntry('❌ Error sending unlock command');
                    alert('Error: ' + err);
                });
        }

        function lockDoor() {
            fetch('/lock', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    updateStatus();
                    addLogEntry('🔒 Lock state reset');
                })
                .catch(err => {
                    addLogEntry('❌ Error resetting lock');
                });
        }

        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('statusText').textContent =
                        data.letmein ? 'Unlocking...' : 'Locked';
                    document.getElementById('lastCommand').textContent =
                        data.last_command_time || 'None';
                    document.getElementById('status').className =
                        'status ' + (data.letmein ? 'unlocked' : 'locked');
                })
                .catch(err => {
                    addLogEntry('⚠️ Connection error');
                });
        }

        // Update status every 2 seconds
        setInterval(updateStatus, 2000);
        updateStatus();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Web interface for controlling the door"""
    return render_template_string(WEB_INTERFACE)

@app.route('/status')
@app.route('/api/status')
def status():
    """API endpoint for Raspberry Pi client to poll - returns JSON status"""
    return jsonify(door_state)

@app.route('/unlock', methods=['POST'])
def unlock():
    """Trigger door unlock"""
    door_state['letmein'] = True
    door_state['last_command_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Log the unlock request
    ip = request.remote_addr
    print(f"[{door_state['last_command_time']}] Unlock triggered from {ip}")

    # Auto-reset after 15 seconds (safety feature)
    def reset_state():
        door_state['letmein'] = False
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Auto-reset: Lock state returned to False")

    Timer(15.0, reset_state).start()

    return jsonify({
        "status": "unlock_triggered",
        "time": door_state['last_command_time'],
        "message": "Door will unlock on next client poll"
    })

@app.route('/lock', methods=['POST'])
def lock():
    """Reset lock state manually"""
    door_state['letmein'] = False
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = request.remote_addr
    print(f"[{timestamp}] Lock state reset from {ip}")
    return jsonify({"status": "locked", "time": timestamp})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "server": "newyakko.cs.wmich.edu",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚪 Doorbot Server Starting")
    print("=" * 60)
    print(f"Server: newyakko.cs.wmich.edu")
    print(f"Port: 8878")
    print(f"Web Interface: http://newyakko.cs.wmich.edu:8878")
    print(f"API Endpoint: http://newyakko.cs.wmich.edu:8878/status")
    print("=" * 60)

    # Listen on all interfaces, port 8878 (same as original)
    app.run(host='0.0.0.0', port=8878, debug=False)
