# Manual SD Card Setup Guide

**For those who prefer to understand and configure manually**

---

## Overview

This guide walks you through manually preparing your Raspberry Pi SD card so the doorbot client runs automatically on boot, without any additional configuration needed after you insert the SD card.

---

## What You'll Do

1. Mount the SD card on your computer
2. Copy the client script to the correct location
3. Create a systemd service file for auto-start
4. (Optional) Configure WiFi
5. Eject and test

**Time required:** 10-15 minutes

---

## Prerequisites

- [ ] Raspberry Pi SD card with working OS
- [ ] SD card reader for your computer
- [ ] Text editor (nano, vim, VS Code, etc.)
- [ ] Root/sudo access on your computer

---

## Step 1: Mount the SD Card

### On Linux:

1. Insert SD card into your computer
2. Find the mount point:
   ```bash
   lsblk
   ```
   Look for your SD card (usually `mmcblk0` or `sdb`)

3. The partitions should auto-mount to:
   - Boot: `/media/YOUR_USER/boot`
   - Root: `/media/YOUR_USER/rootfs`

4. If not auto-mounted:
   ```bash
   sudo mount /dev/mmcblk0p2 /mnt/rootfs
   sudo mount /dev/mmcblk0p1 /mnt/boot
   ```

### On macOS:

1. Insert SD card
2. It should auto-mount to:
   - Boot: `/Volumes/boot`
   - Root: `/Volumes/rootfs` (if supported)

3. If rootfs doesn't mount, install `ext4fuse`:
   ```bash
   brew install ext4fuse
   sudo ext4fuse /dev/disk2s2 /Volumes/rootfs -o allow_other
   ```

### On Windows:

1. Install "Linux File Systems for Windows" or use WSL2
2. Or: Make changes in Linux first, then image to SD card

---

## Step 2: Identify the User

Check which user exists on the Pi:

```bash
ls /media/YOUR_USER/rootfs/home/
```

Common users:
- `pi` (default on Raspberry Pi OS)
- `Janus` (your specific setup)

**For this guide, we'll use `Janus`. Adjust if different.**

---

## Step 3: Copy the Client Script

### Create the directory:

```bash
sudo mkdir -p /media/YOUR_USER/rootfs/home/Janus/doorbot
```

### Copy the client:

```bash
sudo cp doorbot_client.py /media/YOUR_USER/rootfs/home/Janus/doorbot/
```

### Make it executable:

```bash
sudo chmod +x /media/YOUR_USER/rootfs/home/Janus/doorbot/doorbot_client.py
```

### Set ownership (UID 1000 is usually the first user):

```bash
sudo chown -R 1000:1000 /media/YOUR_USER/rootfs/home/Janus/doorbot
```

---

## Step 4: Create the systemd Service

### Create the service file:

```bash
sudo nano /media/YOUR_USER/rootfs/etc/systemd/system/doorbot-client.service
```

### Paste this content:

```ini
[Unit]
Description=Doorbot Client - Door Lock Controller
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=Janus
WorkingDirectory=/home/Janus/doorbot
ExecStart=/usr/bin/python3 /home/Janus/doorbot/doorbot_client.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Important:** Replace `Janus` with your actual username if different.

### Save and exit:
- nano: `Ctrl+O`, `Enter`, `Ctrl+X`
- vim: `:wq`

---

## Step 5: Enable the Service

Create a symlink to enable auto-start:

```bash
sudo mkdir -p /media/YOUR_USER/rootfs/etc/systemd/system/multi-user.target.wants

sudo ln -sf /etc/systemd/system/doorbot-client.service \
    /media/YOUR_USER/rootfs/etc/systemd/system/multi-user.target.wants/doorbot-client.service
```

This tells systemd to start the service on boot.

---

## Step 6: Verify Server URL in Client

Double-check the client has the correct server URL:

```bash
grep "SERVER_URL" /media/YOUR_USER/rootfs/home/Janus/doorbot/doorbot_client.py
```

Should show:
```python
SERVER_URL = "http://newyakko.cs.wmich.edu:8878"
```

If you need to change it:
```bash
sudo nano /media/YOUR_USER/rootfs/home/Janus/doorbot/doorbot_client.py
```

---

## Step 7: Configure WiFi (If Needed)

### Check existing WiFi config:

```bash
sudo cat /media/YOUR_USER/rootfs/etc/NetworkManager/system-connections/preconfigured.nmconnection
```

### If it exists and has the right credentials, skip this step.

### Otherwise, create/edit it:

```bash
sudo nano /media/YOUR_USER/rootfs/etc/NetworkManager/system-connections/preconfigured.nmconnection
```

### Paste this content (update SSID and password):

```ini
[connection]
id=preconfigured
uuid=12345678-1234-1234-1234-123456789abc
type=wifi
autoconnect=true

[wifi]
mode=infrastructure
ssid=YOUR_WIFI_SSID

[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=YOUR_WIFI_PASSWORD

[ipv4]
method=auto

[ipv6]
addr-gen-mode=stable-privacy
method=auto
```

**Replace:**
- `YOUR_WIFI_SSID` with your WiFi network name (e.g., `morgana`)
- `YOUR_WIFI_PASSWORD` with your WiFi password

### Set permissions:

```bash
sudo chmod 600 /media/YOUR_USER/rootfs/etc/NetworkManager/system-connections/preconfigured.nmconnection
```

---

## Step 8: Create a Helpful README

Create a reference file on the Pi's desktop:

```bash
sudo mkdir -p /media/YOUR_USER/rootfs/home/Janus/Desktop

sudo nano /media/YOUR_USER/rootfs/home/Janus/Desktop/DOORBOT_README.txt
```

Paste:

```
==============================================
🚪 DOORBOT CLIENT - QUICK REFERENCE
==============================================

Your Raspberry Pi is configured and ready!

SERVER: http://newyakko.cs.wmich.edu:8878

The doorbot client runs automatically in the background.

USEFUL COMMANDS:
----------------

# Check if client is running
sudo systemctl status doorbot-client

# View live logs
sudo journalctl -u doorbot-client -f

# Restart the client
sudo systemctl restart doorbot-client

# Test server connection
curl http://newyakko.cs.wmich.edu:8878/status


TESTING:
--------

1. Open http://newyakko.cs.wmich.edu:8878
2. Click "Unlock Door"
3. Watch logs: sudo journalctl -u doorbot-client -f
4. Motor should activate within 1 second


CONFIGURATION:
--------------

Client: /home/Janus/doorbot/doorbot_client.py
Service: /etc/systemd/system/doorbot-client.service

To change settings:
  nano ~/doorbot/doorbot_client.py
  sudo systemctl restart doorbot-client


TROUBLESHOOTING:
----------------

If not working, check:

1. Service status:
   sudo systemctl status doorbot-client

2. Logs for errors:
   sudo journalctl -u doorbot-client -n 50

3. Server reachability:
   curl http://newyakko.cs.wmich.edu:8878/health

4. WiFi connection:
   nmcli device status


==============================================
```

Set ownership:
```bash
sudo chown 1000:1000 /media/YOUR_USER/rootfs/home/Janus/Desktop/DOORBOT_README.txt
```

---

## Step 9: Final Verification

Before ejecting, verify all files are in place:

```bash
# Client script exists
ls -l /media/YOUR_USER/rootfs/home/Janus/doorbot/doorbot_client.py

# Service file exists
ls -l /media/YOUR_USER/rootfs/etc/systemd/system/doorbot-client.service

# Service is enabled (symlink exists)
ls -l /media/YOUR_USER/rootfs/etc/systemd/system/multi-user.target.wants/doorbot-client.service

# WiFi config exists (if you created it)
ls -l /media/YOUR_USER/rootfs/etc/NetworkManager/system-connections/preconfigured.nmconnection

# README exists
ls -l /media/YOUR_USER/rootfs/home/Janus/Desktop/DOORBOT_README.txt
```

All should show files with proper ownership.

---

## Step 10: Safely Eject

### On Linux:
```bash
sync
sudo umount /media/YOUR_USER/boot
sudo umount /media/YOUR_USER/rootfs
```

### On macOS:
```bash
diskutil eject /Volumes/boot
diskutil eject /Volumes/rootfs
```

### Or use the GUI eject button

---

## Step 11: Boot and Test

1. **Insert SD card into Raspberry Pi**

2. **Connect power**

3. **Wait ~30-60 seconds for boot**

4. **Check if it's online:**
   - Check your router for the Pi's IP address
   - Or use: `arp -a | grep -i "b8:27:eb"` (Pi MAC prefix)

5. **SSH to the Pi:**
   ```bash
   ssh Janus@RASPBERRY_PI_IP
   ```

6. **Check service status:**
   ```bash
   sudo systemctl status doorbot-client
   ```

   Should show: **active (running)**

7. **Watch the logs:**
   ```bash
   sudo journalctl -u doorbot-client -f
   ```

   Should see:
   ```
   🚪 DOORBOT CLIENT
   Server: http://newyakko.cs.wmich.edu:8878
   Initializing GPIO pins...
   Starting server polling...
   ```

8. **Test the unlock:**
   - Open http://newyakko.cs.wmich.edu:8878 in browser
   - Click "Unlock Door"
   - Watch logs show unlock sequence
   - Motor should activate

---

## Troubleshooting

### Service won't start

```bash
# Check for errors
sudo journalctl -u doorbot-client -n 50

# Try running manually
python3 /home/Janus/doorbot/doorbot_client.py
```

Common issues:
- Python packages not installed: `sudo apt-get install python3-rpi.gpio python3-requests`
- GPIO permissions: `sudo usermod -a -G gpio Janus`
- Wrong paths in service file

### WiFi not connecting

```bash
# Check WiFi status
nmcli device status

# Check config
sudo cat /etc/NetworkManager/system-connections/preconfigured.nmconnection

# Restart NetworkManager
sudo systemctl restart NetworkManager
```

### Can't reach server

```bash
# Test DNS
ping newyakko.cs.wmich.edu

# Test server
curl http://newyakko.cs.wmich.edu:8878/health
```

---

## File Structure Summary

After setup, your SD card should have:

```
/home/Janus/
├── doorbot/
│   └── doorbot_client.py          # Main client script
├── Desktop/
│   └── DOORBOT_README.txt          # Quick reference

/etc/systemd/system/
├── doorbot-client.service          # Service definition
└── multi-user.target.wants/
    └── doorbot-client.service      # Symlink for auto-start

/etc/NetworkManager/system-connections/
└── preconfigured.nmconnection      # WiFi credentials
```

---

## What Happens on Boot

1. Pi boots up
2. NetworkManager connects to WiFi
3. systemd starts `doorbot-client.service`
4. Client script initializes GPIO
5. Client begins polling server every 1 second
6. When you click "Unlock", client receives command and unlocks door

**All automatic, no user intervention needed!**

---

## Next Steps

Now that setup is complete:

- Keep the SD card as a "golden image"
- Clone it if you need multiple Pis
- Document any custom changes you make
- Consider security enhancements if exposing to internet

---

**Your SD card is now plug-and-play! Just insert and boot. 🎉**
