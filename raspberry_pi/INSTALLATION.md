# Raspberry Pi Client Installation Guide

**Complete step-by-step instructions for installing the Doorbot client on your Raspberry Pi**

---

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Raspberry Pi (any model with GPIO pins)
- [ ] Raspbian/Raspberry Pi OS installed
- [ ] SD card with working OS
- [ ] Network connection (WiFi "morgana" or Ethernet)
- [ ] SSH access OR keyboard/monitor connected
- [ ] Server running at `newyakko.cs.wmich.edu:8878`

---

## 🚀 Quick Installation (Automatic)

**If you just want it to work, follow these steps:**

### Step 1: Get the Files onto Your Raspberry Pi

**Option A: Using USB Drive**
1. Copy the entire `raspberry_pi` folder to a USB drive
2. Insert USB drive into Raspberry Pi
3. Mount the drive (usually auto-mounts to `/media/pi/...`)
4. Open terminal and navigate to the folder

**Option B: Using Git** (if server is already on GitHub)
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/doorbot2.git
cd doorbot2/raspberry_pi
```

**Option C: Using SCP** (from another computer)
```bash
# From your computer:
scp -r raspberry_pi/ pi@RASPBERRY_PI_IP:~/
```

### Step 2: Run the Installer

```bash
cd raspberry_pi  # Or wherever you copied the files
chmod +x install_client.sh
./install_client.sh
```

**The installer will:**
- ✓ Check if you're on a Raspberry Pi
- ✓ Install Python dependencies (RPi.GPIO, requests)
- ✓ Copy the client to `/home/YOUR_USER/doorbot/`
- ✓ Test server connectivity
- ✓ Create systemd service
- ✓ Enable auto-start on boot
- ✓ Ask if you want to start now

### Step 3: Verify It's Working

```bash
# Check service status
sudo systemctl status doorbot-client

# Watch live logs
sudo journalctl -u doorbot-client -f
```

You should see:
```
🚪 DOORBOT CLIENT
Server: http://newyakko.cs.wmich.edu:8878
Started: 2026-02-01 18:00:00
Initializing GPIO pins...
Starting server polling...
```

**Done! The client is now running and will auto-start on every boot.**

---

## 🔧 Manual Installation (Step-by-Step)

If the automatic installer doesn't work, or you want to understand each step:

### Step 1: Install Dependencies

```bash
# Update package list
sudo apt-get update

# Install Python 3 and pip (usually pre-installed)
sudo apt-get install -y python3 python3-pip

# Install required Python libraries
sudo apt-get install -y python3-rpi.gpio python3-requests

# Verify installation
python3 --version
python3 -c "import RPi.GPIO; import requests; print('✓ Libraries installed')"
```

### Step 2: Create Installation Directory

```bash
mkdir -p ~/doorbot
cd ~/doorbot
```

### Step 3: Copy the Client Script

Copy `doorbot_client.py` to `~/doorbot/doorbot_client.py`

Make it executable:
```bash
chmod +x ~/doorbot/doorbot_client.py
```

### Step 4: Test the Client Manually

```bash
python3 ~/doorbot/doorbot_client.py
```

You should see:
- GPIO initialization messages
- Server polling messages
- No error messages

Press `Ctrl+C` to stop.

### Step 5: Create systemd Service

Create the service file:
```bash
sudo nano /etc/systemd/system/doorbot-client.service
```

Paste this content (replace `pi` with your username if different):
```ini
[Unit]
Description=Doorbot Client - Door Lock Controller
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/doorbot
ExecStart=/usr/bin/python3 /home/pi/doorbot/doorbot_client.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+O, Enter, Ctrl+X in nano).

### Step 6: Enable and Start Service

```bash
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable doorbot-client.service

# Start the service now
sudo systemctl start doorbot-client.service

# Check status
sudo systemctl status doorbot-client.service
```

---

## 🧪 Testing Your Installation

### Test 1: Check Service Status

```bash
sudo systemctl status doorbot-client
```

Expected output:
```
● doorbot-client.service - Doorbot Client - Door Lock Controller
     Loaded: loaded (/etc/systemd/system/doorbot-client.service; enabled)
     Active: active (running) since ...
```

### Test 2: Check Logs

```bash
sudo journalctl -u doorbot-client -n 50 --no-pager
```

Look for:
- ✓ "DOORBOT CLIENT" banner
- ✓ "Initializing GPIO pins..."
- ✓ "Starting server polling..."
- ❌ NO connection errors
- ❌ NO GPIO errors

### Test 3: Test Server Connection

```bash
curl http://newyakko.cs.wmich.edu:8878/status
```

Expected response:
```json
{"letmein": false, "last_command_time": null, "last_unlock_user": null}
```

### Test 4: Test Full Unlock Sequence

1. Open web interface: http://newyakko.cs.wmich.edu:8878
2. Click "Unlock Door"
3. Watch the logs in real-time:
   ```bash
   sudo journalctl -u doorbot-client -f
   ```
4. Within 1 second, you should see:
   ```
   🔓 UNLOCKING DOOR
   Activating power relay...
   Starting motor (unlock direction)...
   ```

### Test 5: Verify Auto-Start on Reboot

```bash
# Reboot the Pi
sudo reboot

# After reboot, check if service started automatically
sudo systemctl status doorbot-client
```

---

## 📱 Command Reference

### Service Management

```bash
# Start the service
sudo systemctl start doorbot-client

# Stop the service
sudo systemctl stop doorbot-client

# Restart the service
sudo systemctl restart doorbot-client

# Check status
sudo systemctl status doorbot-client

# Enable auto-start on boot
sudo systemctl enable doorbot-client

# Disable auto-start
sudo systemctl disable doorbot-client
```

### Viewing Logs

```bash
# View last 50 log lines
sudo journalctl -u doorbot-client -n 50

# Follow logs in real-time (Ctrl+C to exit)
sudo journalctl -u doorbot-client -f

# View logs from today
sudo journalctl -u doorbot-client --since today

# View logs with timestamps
sudo journalctl -u doorbot-client -o short-precise

# Clear old logs (if disk space is an issue)
sudo journalctl --vacuum-time=7d
```

### Manual Testing

```bash
# Run client manually (service must be stopped first)
sudo systemctl stop doorbot-client
python3 ~/doorbot/doorbot_client.py

# Test GPIO permissions
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('✓ GPIO OK')"

# Test server connection
curl http://newyakko.cs.wmich.edu:8878/health
```

---

## 🔄 Updating the Client

If you need to update the client code:

```bash
# Stop the service
sudo systemctl stop doorbot-client

# Edit the file
nano ~/doorbot/doorbot_client.py

# Save and exit

# Restart the service
sudo systemctl start doorbot-client

# Check logs for errors
sudo journalctl -u doorbot-client -f
```

---

## 🗑️ Uninstalling

To completely remove the doorbot client:

```bash
# Stop and disable service
sudo systemctl stop doorbot-client
sudo systemctl disable doorbot-client

# Remove service file
sudo rm /etc/systemd/system/doorbot-client.service

# Reload systemd
sudo systemctl daemon-reload

# Remove client directory
rm -rf ~/doorbot

# (Optional) Remove Python packages
sudo apt-get remove python3-rpi.gpio python3-requests
```

---

## ⚙️ Configuration Options

You can modify these settings in `doorbot_client.py`:

```python
# Line 27: Server URL
SERVER_URL = "http://newyakko.cs.wmich.edu:8878"

# Line 28: How often to poll server (in seconds)
POLL_INTERVAL = 1.0

# Lines 31-34: GPIO Pin assignments
RELAY_PIN = 4
DIRECTION_PIN = 15
PWM_PIN = 18
BUTTON_PIN = 7

# Line 37: Motor PWM frequency
PWM_FREQUENCY = 500

# Line 39: How long to hold door unlocked (seconds)
UNLOCK_HOLD_TIME = 10
```

After changing, restart the service:
```bash
sudo systemctl restart doorbot-client
```

---

## 🆘 Need Help?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

For detailed system architecture, see [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md).
