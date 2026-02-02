# 🚪 Doorbot2 - Remote Door Lock System

**Replacement server for the Raspberry Pi-based remote door lock system**

Migrated from `dot.cs.wmich.edu:8878` to `newyakko.cs.wmich.edu:8878`

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)

---

## 📖 What Is This?

This is a complete remote door lock system that allows you to unlock a physical door via:
- 💬 **Element chatbot command** (`$letmein`) - Primary method
- 🌐 **Web interface** - Manual backup option
- 🔌 **API calls** - Integration-ready

**System Components:**
- 🖥️ **Flask Server** - Runs on newyakko.cs.wmich.edu:8878
- 🍓 **Raspberry Pi Client** - Controls door lock hardware via GPIO
- 🤖 **Element Chatbot** - Sends unlock commands from chat

---

## 🚀 Quick Start

### For First-Time Setup (5 Minutes)

1. **Prepare the SD Card** (plug-and-play method)
   ```bash
   cd raspberry_pi
   ./prepare_sd_card.sh
   ```
   Insert SD card, run script, done!

2. **Deploy Server on newyakko.cs.wmich.edu**
   ```bash
   git clone https://github.com/airbreak404/doorbot2.git
   cd doorbot2
   pip3 install -r requirements.txt
   python3 server.py
   ```

3. **Update Element Chatbot**
   - See [chatbot_command/README.md](chatbot_command/README.md)
   - Change URL from `dot.cs.wmich.edu:8878` to `newyakko.cs.wmich.edu:8878`

4. **Test It!**
   - Insert SD card in Pi and boot
   - In Element chat: `$letmein`
   - Door unlocks! 🎉

**👉 Detailed Instructions:** [MIGRATION_FROM_DOT.md](MIGRATION_FROM_DOT.md)

---

## 📚 Complete Documentation

### 🎯 Start Here
| Document | Purpose |
|----------|---------|
| **[MIGRATION_FROM_DOT.md](MIGRATION_FROM_DOT.md)** | **Complete migration guide** from dot to newyakko |
| **[raspberry_pi/QUICK_START.md](raspberry_pi/QUICK_START.md)** | **3-step setup** for Raspberry Pi |
| **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** | System architecture and how everything works |

### 🍓 Raspberry Pi Setup
| Document | Purpose |
|----------|---------|
| **[raspberry_pi/README.md](raspberry_pi/README.md)** | Client overview and setup options |
| **[raspberry_pi/prepare_sd_card.sh](raspberry_pi/prepare_sd_card.sh)** | **Automated SD card setup** (RECOMMENDED) |
| **[raspberry_pi/INSTALLATION.md](raspberry_pi/INSTALLATION.md)** | Detailed installation instructions |
| **[raspberry_pi/SD_CARD_MANUAL_SETUP.md](raspberry_pi/SD_CARD_MANUAL_SETUP.md)** | Manual SD card configuration |
| **[raspberry_pi/TROUBLESHOOTING.md](raspberry_pi/TROUBLESHOOTING.md)** | Problem solutions |

### 🤖 Chatbot Integration
| Document | Purpose |
|----------|---------|
| **[chatbot_command/README.md](chatbot_command/README.md)** | Update Element chatbot command |
| **[chatbot_command/letmein.py](chatbot_command/letmein.py)** | Updated command file |

### 🔧 Server Setup
| File | Purpose |
|------|---------|
| **[server.py](server.py)** | Main Flask server application |
| **[doorbot-server.service](doorbot-server.service)** | systemd service for auto-start |
| **[setup.sh](setup.sh)** | Automated server setup |
| **[test_server.sh](test_server.sh)** | Server testing script |

---

## 🌐 Server Information

- **Host:** newyakko.cs.wmich.edu
- **Port:** 8878
- **Web Control:** http://newyakko.cs.wmich.edu:8878/control
- **Health Check:** http://newyakko.cs.wmich.edu:8878/health
- **API Endpoint:** http://newyakko.cs.wmich.edu:8878/

### API Specification

| Method | Endpoint | Purpose | Used By |
|--------|----------|---------|---------|
| `GET /` | Returns `{"letmein": bool}` | Pi client polls for status | Raspberry Pi |
| `POST /` | Accepts `{"status": {"letmein": bool}}` | Control door lock | Element chatbot |
| `GET /control` | Web interface | Manual control | Web browser |
| `GET /health` | Server status | Health monitoring | Monitoring tools |

---

## 🎯 How It Works

```
User: "$letmein" in Element chat
        ↓
Chatbot: POST / {"status": {"letmein": true}}
        ↓
Server: Sets letmein = true
        ↓
Raspberry Pi: Polls GET / every 1 second
        ↓
Pi receives: {"letmein": true}
        ↓
Pi: Unlocks door via GPIO
        ↓
Chatbot: After 3s, POST / {"status": {"letmein": false}}
        ↓
Door: Returns to locked state
```

---

## 🛠️ Hardware Requirements

### Raspberry Pi Setup
- Raspberry Pi (any model with GPIO)
- Stepper motor for door handle rotation
- Relay module for power control
- Position sensor (optional but recommended)

### GPIO Pin Assignment
| Pin | Function |
|-----|----------|
| GPIO 4 | Power relay control |
| GPIO 15 | Motor direction control |
| GPIO 18 | Stepper motor PWM |
| GPIO 7 | Handle position sensor |

---

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

## ✅ Testing Your Installation

### 1. Test Server API

```bash
# Test Pi polling endpoint
curl http://newyakko.cs.wmich.edu:8878/

# Expected: {"letmein": false, "last_command_time": null, ...}

# Test chatbot endpoint
curl -X POST http://newyakko.cs.wmich.edu:8878/ \
  -H "Content-Type: application/json" \
  -d '{"status": {"letmein": true}}'

# Expected: {"success": true, "letmein": true}
```

### 2. Test Raspberry Pi Client

```bash
# SSH to the Pi
ssh Janus@RASPBERRY_PI_IP

# Check if service is running
sudo systemctl status doorbot-client

# Watch logs in real-time
sudo journalctl -u doorbot-client -f
```

### 3. Test Element Chatbot

In your Element chat:
```
$letmein
```

Expected response: "Door unlocked and now locked again."

### 4. Complete End-to-End Test

1. Start server on newyakko
2. Boot Raspberry Pi with prepared SD card
3. In Element chat: `$letmein`
4. Watch Pi logs for unlock sequence
5. Verify door physically unlocks

**Success!** Your Doorbot system is fully operational. 🎉

---

## 🚢 Deployment

### Production Deployment (systemd service)

```bash
# Copy service file
sudo cp doorbot-server.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable doorbot-server
sudo systemctl start doorbot-server

# Check status
sudo systemctl status doorbot-server

# View logs
sudo journalctl -u doorbot-server -f
```

### Firewall Configuration

```bash
# Allow port 8878
sudo ufw allow 8878/tcp
```

---

## 🐛 Troubleshooting

### Quick Diagnostics

```bash
# Server not responding
sudo systemctl status doorbot-server
sudo journalctl -u doorbot-server -n 50

# Pi can't reach server
ping newyakko.cs.wmich.edu
curl http://newyakko.cs.wmich.edu:8878/health

# Pi client not running
sudo systemctl status doorbot-client
sudo journalctl -u doorbot-client -n 50

# Test hardware
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('OK')"
```

**For detailed troubleshooting:** [raspberry_pi/TROUBLESHOOTING.md](raspberry_pi/TROUBLESHOOTING.md)

---

## 📁 Repository Structure

```
doorbot2/
├── server.py                      # Flask server application
├── requirements.txt               # Python dependencies
├── doorbot-server.service         # systemd service file
├── setup.sh                       # Automated server setup
├── test_server.sh                 # Server testing script
│
├── README.md                      # This file
├── MIGRATION_FROM_DOT.md          # Migration guide from dot to newyakko
├── PROJECT_OVERVIEW.md            # System architecture documentation
├── RASPBERRY_PI_SETUP.md          # Legacy Pi setup guide
├── GITHUB_SETUP.md               # GitHub repository setup
│
├── raspberry_pi/                  # Raspberry Pi client files
│   ├── doorbot_client.py          # Pre-configured client script
│   ├── prepare_sd_card.sh         # Automated SD card preparation
│   ├── install_client.sh          # Installation script
│   ├── README.md                  # Client documentation
│   ├── QUICK_START.md             # Quick start guide
│   ├── INSTALLATION.md            # Detailed installation
│   ├── TROUBLESHOOTING.md         # Problem solutions
│   └── SD_CARD_MANUAL_SETUP.md   # Manual SD card guide
│
└── chatbot_command/               # Element chatbot integration
    ├── letmein.py                 # Updated chatbot command
    └── README.md                  # Chatbot update instructions
```

---

## 🔒 Security Considerations

**⚠️ Current Implementation: NO AUTHENTICATION**

This server has no authentication. Anyone who can access the URL can unlock the door.

**This is acceptable for:**
- Internal networks only
- Trusted environments
- Development/testing

**For production internet exposure, implement:**
- API key authentication
- HTTPS/TLS encryption
- IP whitelisting
- Rate limiting
- User authentication system
- Audit logging

See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for security enhancement examples.

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Authentication system
- [ ] HTTPS support
- [ ] Mobile app integration
- [ ] Database logging
- [ ] Multiple door support
- [ ] Access control lists
- [ ] Webhook notifications
- [ ] Home Assistant integration

---

## 📄 License

This is a restoration/replacement project for an existing system. Use at your own discretion.

---

## 👥 Credits

- **Original System:** Western Michigan University CS Department
- **Server Migration & Documentation:** Doorbot2 Project
- **Original Chatbot Command:** Lochlan McElroy

---

## 📞 Support

- **Documentation:** See links above for comprehensive guides
- **Issues:** Report problems via GitHub Issues
- **Quick Help:** See [raspberry_pi/QUICK_START.md](raspberry_pi/QUICK_START.md)

---

## 🎓 Project History

**Previous Server:** `dot.cs.wmich.edu:8878` (Western Michigan University - decommissioned)

**Current Server:** `newyakko.cs.wmich.edu:8878` (Replacement implementation)

This project maintains API compatibility with the original system while adding improved documentation, easier setup, and enhanced features.

---

**Repository:** https://github.com/airbreak404/doorbot2

**Ready to get started?** → [MIGRATION_FROM_DOT.md](MIGRATION_FROM_DOT.md)
