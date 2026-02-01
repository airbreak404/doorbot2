# Doorbot Server

Replacement server for the Raspberry Pi-based remote door lock system.

## Server Information

- **Host**: newyakko.cs.wmich.edu
- **Port**: 8878
- **Web Interface**: http://newyakko.cs.wmich.edu:8878
- **API Endpoint**: http://newyakko.cs.wmich.edu:8878/status

## Installation

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or manually:
```bash
pip3 install flask
```

### 2. Test the Server

```bash
python3 server.py
```

The server will start on port 8878. You should see:
```
🚪 Doorbot Server Starting
Server: newyakko.cs.wmich.edu
Port: 8878
Web Interface: http://newyakko.cs.wmich.edu:8878
```

### 3. Access the Web Interface

Open a browser and navigate to:
- Local: http://localhost:8878
- Remote: http://newyakko.cs.wmich.edu:8878

## API Endpoints

### GET /status
Returns current door lock state (polled by Raspberry Pi client)

**Response:**
```json
{
    "letmein": false,
    "last_command_time": "2026-02-01 10:30:45",
    "last_unlock_user": null
}
```

### POST /unlock
Triggers door unlock sequence

**Response:**
```json
{
    "status": "unlock_triggered",
    "time": "2026-02-01 10:30:45",
    "message": "Door will unlock on next client poll"
}
```

Auto-resets to locked state after 15 seconds.

### POST /lock
Manually resets lock state to locked

### GET /health
Health check endpoint

## Running as a Service (systemd)

To run the server automatically on boot:

### 1. Create systemd service file

```bash
sudo nano /etc/systemd/system/doorbot-server.service
```

Add the following content:

```ini
[Unit]
Description=Doorbot Server
After=network.target

[Service]
Type=simple
User=airbreak
WorkingDirectory=/home/airbreak/doorbot_server
ExecStart=/usr/bin/python3 /home/airbreak/doorbot_server/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable doorbot-server.service
sudo systemctl start doorbot-server.service
```

### 3. Check service status

```bash
sudo systemctl status doorbot-server.service
```

### 4. View logs

```bash
sudo journalctl -u doorbot-server.service -f
```

## Raspberry Pi Client Configuration

Update the Raspberry Pi client to point to this server:

**File**: `/home/Janus/Downloads/doorbot_client.py`
**Line 49**: Change to:

```python
server_url = "http://newyakko.cs.wmich.edu:8878"
```

## Firewall Configuration

If the server is not accessible, you may need to open port 8878:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 8878/tcp

# firewalld (RedHat/CentOS)
sudo firewall-cmd --permanent --add-port=8878/tcp
sudo firewall-cmd --reload

# iptables
sudo iptables -A INPUT -p tcp --dport 8878 -j ACCEPT
```

## Testing

### Test from command line:

```bash
# Check status
curl http://newyakko.cs.wmich.edu:8878/status

# Trigger unlock
curl -X POST http://newyakko.cs.wmich.edu:8878/unlock

# Reset lock
curl -X POST http://newyakko.cs.wmich.edu:8878/lock

# Health check
curl http://newyakko.cs.wmich.edu:8878/health
```

### Expected workflow:

1. Raspberry Pi polls `/status` every 1 second
2. Web interface user clicks "Unlock Door"
3. Server sets `letmein: true`
4. Pi receives `letmein: true` on next poll
5. Pi executes unlock sequence
6. After 15 seconds, server auto-resets to `letmein: false`

## Troubleshooting

### Server won't start
- Check if port 8878 is already in use: `sudo lsof -i :8878`
- Check Python version: `python3 --version` (requires 3.8+)
- Verify Flask is installed: `python3 -c "import flask"`

### Pi can't connect
- Test connectivity: `curl http://newyakko.cs.wmich.edu:8878/health`
- Check firewall settings
- Verify server is running: `sudo systemctl status doorbot-server`
- Check server logs: `sudo journalctl -u doorbot-server -n 50`

### Web interface not loading
- Check server logs for errors
- Verify you're accessing the correct URL
- Check browser console for JavaScript errors

## Security Notes

Currently, the server has **no authentication**. Anyone who can access the URL can unlock the door.

For production use, consider:
- Adding API key authentication
- Implementing HTTPS
- Adding IP whitelisting
- Implementing rate limiting
- Adding user authentication

See the original plan document for security enhancement examples.

## File Structure

```
/home/airbreak/doorbot_server/
├── server.py           # Main Flask server
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── doorbot-server.service  # systemd service file (optional)
```

## Support

For issues or questions, refer to the comprehensive project plan document.
