# Doorbot Server

Replacement server for the Raspberry Pi-based remote door lock system.

> **🚀 New to this project?** Start with the [Quick Start Guide](raspberry_pi/QUICK_START.md) to get up and running in minutes!

---

## 📚 Documentation Index

### Getting Started
- **[Quick Start Guide](raspberry_pi/QUICK_START.md)** - Get your system working in 3 simple steps
- **[Project Overview](PROJECT_OVERVIEW.md)** - Complete system architecture and documentation
- **[Installation Guide](raspberry_pi/INSTALLATION.md)** - Detailed Raspberry Pi setup instructions

### Raspberry Pi Setup (Choose One Method)
- **[Automated SD Card Setup](raspberry_pi/prepare_sd_card.sh)** - Run this script to make your SD card plug-and-play (RECOMMENDED)
- **[Manual SD Card Setup](raspberry_pi/SD_CARD_MANUAL_SETUP.md)** - Step-by-step manual configuration
- **[Install After Boot](raspberry_pi/install_client.sh)** - Install on a running Raspberry Pi

### Reference
- **[Troubleshooting Guide](raspberry_pi/TROUBLESHOOTING.md)** - Solutions to common problems
- **[Raspberry Pi Client README](raspberry_pi/README.md)** - Complete client documentation
- **[GitHub Setup](GITHUB_SETUP.md)** - How to create the GitHub repository

---

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

## Raspberry Pi Client Setup

The Raspberry Pi client is **pre-configured and ready to use**!

### Option 1: Automated Setup (Recommended)

Run the preparation script to make your SD card plug-and-play:

```bash
cd raspberry_pi
./prepare_sd_card.sh
```

This will:
- Automatically detect your SD card
- Install the client with correct server URL
- Configure auto-start on boot
- Set up WiFi (optional)

Then just insert the SD card and boot - it works immediately!

### Option 2: Manual Configuration

See the [Raspberry Pi Setup Guide](raspberry_pi/README.md) for other installation methods.

The client is pre-configured with:
- Server URL: `http://newyakko.cs.wmich.edu:8878`
- Poll interval: 1 second
- Auto-start on boot

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
doorbot_server/
├── server.py                      # Main Flask server
├── requirements.txt               # Python dependencies
├── setup.sh                       # Automated server setup
├── test_server.sh                 # Server testing script
├── doorbot-server.service         # systemd service file
├── README.md                      # This file
├── PROJECT_OVERVIEW.md            # Complete system documentation
├── RASPBERRY_PI_SETUP.md          # Legacy Pi setup guide
├── GITHUB_SETUP.md               # GitHub repository creation
└── raspberry_pi/                  # Raspberry Pi client files
    ├── doorbot_client.py          # Pre-configured client script
    ├── prepare_sd_card.sh         # Automated SD card setup
    ├── install_client.sh          # Installation script
    ├── README.md                  # Client documentation
    ├── QUICK_START.md             # Quick start guide
    ├── INSTALLATION.md            # Detailed installation
    ├── TROUBLESHOOTING.md         # Problem solutions
    └── SD_CARD_MANUAL_SETUP.md   # Manual SD card guide
```

## Complete System Test

### 1. Start the Server (on newyakko.cs.wmich.edu)

```bash
cd ~/doorbot_server
python3 server.py
```

### 2. Prepare Raspberry Pi SD Card

```bash
cd raspberry_pi
./prepare_sd_card.sh
```

### 3. Boot Raspberry Pi

Insert SD card and power on. Client auto-starts.

### 4. Test the System

1. Open http://newyakko.cs.wmich.edu:8878
2. Click "Unlock Door"
3. Within 1 second, the door should unlock

**Success!** Your Doorbot system is fully operational.

## Support

- **Troubleshooting:** See [raspberry_pi/TROUBLESHOOTING.md](raspberry_pi/TROUBLESHOOTING.md)
- **System Architecture:** See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- **GitHub Issues:** Report problems on GitHub after pushing this repository
