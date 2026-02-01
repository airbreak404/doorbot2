# Raspberry Pi Client Configuration

This document describes how to update the Raspberry Pi client to connect to the new server at newyakko.cs.wmich.edu:8878

## Required Change

**File to modify**: `/home/Janus/Downloads/doorbot_client.py`

**Line 49** - Change from:
```python
server_url = "http://dot.cs.wmich.edu:8878"
```

**To**:
```python
server_url = "http://newyakko.cs.wmich.edu:8878"
```

## Method 1: Edit via SD Card on Mac

1. Power off the Raspberry Pi
2. Remove the SD card
3. Insert SD card into your Mac
4. Wait for volumes to mount
5. Navigate to: `/Volumes/rootfs/home/Janus/Downloads/`
6. Edit `doorbot_client.py` with a text editor
7. Find line 49 and update the server URL
8. Save the file
9. Safely eject the SD card
10. Insert back into Raspberry Pi and power on

## Method 2: Edit via SSH (Recommended)

If the Raspberry Pi can boot and connect to WiFi:

1. Find the Pi's IP address (check your router, or use `arp -a | grep -i b8:27:eb`)
2. SSH into the Pi:
   ```bash
   ssh Janus@RASPBERRY_PI_IP
   ```
   Default password is likely "raspberry" or "Janus"

3. Edit the file:
   ```bash
   nano /home/Janus/Downloads/doorbot_client.py
   ```

4. Find line 49 (press Ctrl+_ then type 49)
5. Change the server URL to: `http://newyakko.cs.wmich.edu:8878`
6. Save: Press Ctrl+O, then Enter
7. Exit: Press Ctrl+X

8. Test the connection:
   ```bash
   curl http://newyakko.cs.wmich.edu:8878/status
   ```
   You should see JSON response like: `{"letmein": false, ...}`

9. Test the client:
   ```bash
   python3 /home/Janus/Downloads/doorbot_client.py
   ```
   You should see "Waiting..." messages if it's polling successfully

10. If it works, press Ctrl+C to stop, then set up auto-start (see below)

## Method 3: Edit via VNC

1. Enable VNC on the Pi (if not already enabled):
   ```bash
   ssh Janus@RASPBERRY_PI_IP
   sudo raspi-config
   # Navigate to: Interface Options → VNC → Enable
   ```

2. Download VNC Viewer: https://www.realvnc.com/en/connect/download/viewer/
3. Connect to the Pi's IP address
4. Open the file manager, navigate to `/home/Janus/Downloads/`
5. Right-click `doorbot_client.py` → Text Editor
6. Edit line 49, save, and close

## Setting Up Auto-Start on Boot

After confirming the client works, set it up to run automatically:

### Option A: systemd Service (Recommended)

1. Create service file:
   ```bash
   sudo nano /etc/systemd/system/doorbot-client.service
   ```

2. Add this content:
   ```ini
   [Unit]
   Description=Doorbot Client
   After=network.target

   [Service]
   Type=simple
   User=Janus
   WorkingDirectory=/home/Janus/Downloads
   ExecStart=/usr/bin/python3 /home/Janus/Downloads/doorbot_client.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable doorbot-client.service
   sudo systemctl start doorbot-client.service
   ```

4. Check status:
   ```bash
   sudo systemctl status doorbot-client.service
   ```

5. View logs:
   ```bash
   sudo journalctl -u doorbot-client.service -f
   ```

### Option B: Crontab

1. Edit crontab:
   ```bash
   crontab -e
   ```

2. Add this line:
   ```
   @reboot sleep 30 && python3 /home/Janus/Downloads/doorbot_client.py >> /home/Janus/doorbot.log 2>&1
   ```

3. Save and exit
4. Reboot to test: `sudo reboot`

## Testing the Complete System

1. Ensure the server is running on newyakko.cs.wmich.edu:8878
2. Start the Raspberry Pi client (manually or via service)
3. Open the web interface: http://newyakko.cs.wmich.edu:8878
4. Click "Unlock Door"
5. Watch the Pi's logs/output - you should see "Unlocking door..." within 1 second
6. The motor should activate and unlock the door

## Troubleshooting

### Client can't connect to server

**Test connectivity from Pi:**
```bash
curl http://newyakko.cs.wmich.edu:8878/health
```

If this fails:
- Check if newyakko.cs.wmich.edu is reachable: `ping newyakko.cs.wmich.edu`
- Verify port 8878 is open on the server
- Check Pi's internet connection
- Verify WiFi is connected (SSID: "morgana")

### Client is polling but motor not running

**Check GPIO permissions:**
```bash
sudo usermod -a -G gpio Janus
```

**Test hardware separately:**
```bash
python3 /home/Janus/Downloads/Relaytest.py
python3 /home/Janus/Downloads/steppertest.py
```

### WiFi not connecting

WiFi credentials are in:
```
/etc/NetworkManager/system-connections/preconfigured.nmconnection
```

SSID is "morgana" - verify password is correct.

## Complete Client Code Reference

For reference, the client polls this endpoint:
```
GET http://newyakko.cs.wmich.edu:8878/status
```

And expects this JSON response:
```json
{
    "letmein": true,   // or false
    "last_command_time": "2026-02-01 10:30:45",
    "last_unlock_user": null
}
```

When `letmein` is `true`, the client executes the unlock sequence.

## Quick Command Reference

```bash
# SSH into Pi
ssh Janus@RASPBERRY_PI_IP

# Edit client code
nano /home/Janus/Downloads/doorbot_client.py

# Test server connectivity
curl http://newyakko.cs.wmich.edu:8878/status

# Run client manually
python3 /home/Janus/Downloads/doorbot_client.py

# Check client service status
sudo systemctl status doorbot-client

# View client logs
sudo journalctl -u doorbot-client -f

# Restart client service
sudo systemctl restart doorbot-client

# Check WiFi connection
nmcli device status
```
