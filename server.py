#!/usr/bin/env python3
"""
Doorbot Server - Replacement for dot.cs.wmich.edu:8878

This server replicates the original API to work with:
- Raspberry Pi client polling for door unlock status
- Element chatbot $letmein command

API Endpoints:
- GET  /  → Returns {"letmein": true/false} for Pi client polling
- POST /  → Accepts {"status": {"letmein": true/false}} from chatbot
"""

from flask import Flask, jsonify, render_template_string, request
from datetime import datetime

app = Flask(__name__)

# State management
door_state = {
    "letmein": False,
    "last_command_time": None,
    "last_unlock_user": None,
    "sound": "",
    "sounds": []
}

# Web interface HTML
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
        .info {
            margin-top: 20px;
            padding: 15px;
            background: #fff3cd;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚪 Doorbot Control Panel</h1>

        <div class="info">
            <strong>💬 Preferred Method:</strong> Use the Element chatbot command <code>$letmein</code> in your chat
        </div>

        <div>
            <button class="button unlock-btn" onclick="unlockDoor()">Unlock Door (Manual)</button>
            <button class="button lock-btn" onclick="lockDoor()">Reset Lock State</button>
        </div>

        <div id="status" class="status">
            <strong>Status:</strong> <span id="statusText">Locked</span><br>
            <strong>Last command:</strong> <span id="lastCommand">None</span><br>
            <strong>Server:</strong> newyakko.cs.wmich.edu:8878
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
            // Mimic the chatbot command behavior
            const data = {
                status: {
                    letmein: true
                }
            };

            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                updateStatus();
                addLogEntry('✅ Unlock command sent (manual)');

                // Auto-reset after 3 seconds (like the chatbot does)
                setTimeout(() => {
                    const resetData = {
                        status: {
                            letmein: false
                        }
                    };
                    fetch('/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(resetData)
                    })
                    .then(() => {
                        updateStatus();
                        addLogEntry('🔒 Auto-reset to locked');
                    });
                }, 3000);
            })
            .catch(err => {
                addLogEntry('❌ Error sending unlock command');
            });
        }

        function lockDoor() {
            const data = {
                status: {
                    letmein: false
                }
            };

            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
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
            fetch('/')
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

@app.route('/', methods=['GET', 'POST'])
def root_endpoint():
    """
    Main endpoint - handles both Pi client polling and chatbot commands

    GET: Returns door status for Raspberry Pi client polling
    POST: Accepts door control commands from Element chatbot
    """

    if request.method == 'GET':
        # Raspberry Pi client polling for status
        # Return simple JSON with letmein status
        return jsonify(door_state)

    elif request.method == 'POST':
        # Element chatbot sending unlock/lock command
        # Expected format: {"status": {"letmein": true/false}}

        try:
            data = request.get_json()

            if data and 'status' in data and 'letmein' in data['status']:
                # Update the letmein status
                door_state['letmein'] = data['status']['letmein']
                door_state['sound'] = data['status'].get('sound', '')
                door_state['last_command_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Log the command
                ip = request.remote_addr
                action = "UNLOCK" if door_state['letmein'] else "LOCK"
                print(f"[{door_state['last_command_time']}] {action} command from {ip}")

                return jsonify({"success": True, "letmein": door_state['letmein']}), 200
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Invalid POST data: {data}")
                return jsonify({"error": "Invalid data format"}), 400

        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error processing POST: {e}")
            return jsonify({"error": str(e)}), 500

@app.route('/sounds', methods=['GET', 'POST'])
def sounds_endpoint():
    """
    GET  /sounds → Returns the current sound list
    POST /sounds → Pi client registers its available sounds
    """
    if request.method == 'GET':
        return jsonify({"sounds": door_state['sounds']})

    # POST — Pi client pushing its sound list
    try:
        data = request.get_json()
        if data and 'sounds' in data:
            door_state['sounds'] = data['sounds']
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sound list updated: {len(data['sounds'])} sounds")
            return jsonify({"success": True, "count": len(data['sounds'])}), 200
        return jsonify({"error": "Missing 'sounds' field"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/control')
def web_interface():
    """Web interface for manual control"""
    return render_template_string(WEB_INTERFACE)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "server": "newyakko.cs.wmich.edu",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "current_state": door_state
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚪 Doorbot Server Starting")
    print("=" * 60)
    print(f"Server: newyakko.cs.wmich.edu")
    print(f"Port: 8878")
    print(f"")
    print(f"API Endpoints:")
    print(f"  GET  / → Pi client polls for status")
    print(f"  POST / → Chatbot sends unlock commands")
    print(f"  GET  /control → Web interface")
    print(f"  GET  /health → Health check")
    print(f"")
    print(f"Element chatbot command: $letmein")
    print("=" * 60)

    # Listen on all interfaces, port 8878 (same as original)
    app.run(host='0.0.0.0', port=8878, debug=False)
