# 🔧 Doorbot Troubleshooting Guide

**Comprehensive solutions to common issues**

---

## 🚨 Quick Diagnostic Commands

Run these first to get an overview of the system:

```bash
# Check if client service is running
sudo systemctl status doorbot-client

# View recent logs
sudo journalctl -u doorbot-client -n 50 --no-pager

# Test server connectivity
curl http://newyakko.cs.wmich.edu:8878/health

# Check network connectivity
ping -c 3 newyakko.cs.wmich.edu

# Verify GPIO access
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('GPIO OK')"

# Check WiFi status
nmcli device status
```

---

## 📊 Problem Categories

### 1. Server Issues
### 2. Network/Connectivity Issues
### 3. Raspberry Pi Client Issues
### 4. Hardware/GPIO Issues
### 5. Service/Startup Issues

---

## 1️⃣ Server Issues

### Problem: Cannot access http://newyakko.cs.wmich.edu:8878

**Symptoms:**
- Browser shows "Connection refused" or "Site can't be reached"
- `curl` commands fail

**Diagnostics:**
```bash
# Test from any computer
curl -v http://newyakko.cs.wmich.edu:8878/health

# Check if server is reachable
ping newyakko.cs.wmich.edu

# Check if port 8878 is accessible
nc -zv newyakko.cs.wmich.edu 8878
```

**Solutions:**

1. **Server not running**
   ```bash
   # SSH to newyakko.cs.wmich.edu
   ssh user@newyakko.cs.wmich.edu

   # Check if server is running
   sudo systemctl status doorbot-server

   # Start it if not running
   sudo systemctl start doorbot-server

   # Or run manually
   cd ~/doorbot_server
   python3 server.py
   ```

2. **Firewall blocking port 8878**
   ```bash
   # On the server machine
   sudo ufw allow 8878/tcp
   # OR
   sudo firewall-cmd --permanent --add-port=8878/tcp
   sudo firewall-cmd --reload
   ```

3. **Server crashed/has errors**
   ```bash
   # Check server logs
   sudo journalctl -u doorbot-server -n 100

   # Try running manually to see errors
   cd ~/doorbot_server
   python3 server.py
   ```

4. **Flask not installed**
   ```bash
   pip3 install flask
   ```

### Problem: Web interface loads but buttons don't work

**Symptoms:**
- Page loads but clicking "Unlock" does nothing
- JavaScript errors in browser console

**Solutions:**

1. **Check browser console** (F12 → Console tab)
   - Look for JavaScript errors
   - Look for network request failures

2. **Test API directly**
   ```bash
   # This should work:
   curl -X POST http://newyakko.cs.wmich.edu:8878/unlock

   # Should return JSON with status
   ```

3. **Clear browser cache**
   - Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)

---

## 2️⃣ Network/Connectivity Issues

### Problem: Raspberry Pi can't reach server

**Symptoms:**
- Client logs show "Cannot connect to server"
- `curl` from Pi fails

**Diagnostics:**
```bash
# On the Raspberry Pi:

# Test basic connectivity
ping -c 3 newyakko.cs.wmich.edu

# Test DNS resolution
nslookup newyakko.cs.wmich.edu

# Test server HTTP connection
curl -v http://newyakko.cs.wmich.edu:8878/health

# Check route
traceroute newyakko.cs.wmich.edu
```

**Solutions:**

1. **No network connection**
   ```bash
   # Check network interfaces
   ip addr show

   # Check if WiFi is connected
   nmcli device status

   # Restart NetworkManager
   sudo systemctl restart NetworkManager
   ```

2. **WiFi not connecting**
   ```bash
   # Check WiFi configuration
   sudo cat /etc/NetworkManager/system-connections/preconfigured.nmconnection

   # Scan for networks
   sudo nmcli device wifi list

   # Connect manually
   sudo nmcli device wifi connect "SSID" password "PASSWORD"
   ```

3. **Wrong WiFi password**
   ```bash
   # Edit WiFi config
   sudo nano /etc/NetworkManager/system-connections/preconfigured.nmconnection

   # Change psk= line to correct password
   # Save and restart NetworkManager
   sudo systemctl restart NetworkManager
   ```

4. **DNS not resolving**
   ```bash
   # Add to /etc/hosts as temporary fix
   echo "SERVER_IP  newyakko.cs.wmich.edu" | sudo tee -a /etc/hosts

   # Or configure DNS
   sudo nano /etc/resolv.conf
   # Add: nameserver 8.8.8.8
   ```

### Problem: Intermittent connection drops

**Symptoms:**
- Client works sometimes, fails other times
- "Timeout" errors in logs

**Solutions:**

1. **WiFi signal weak**
   ```bash
   # Check signal strength
   iwconfig wlan0

   # Move Pi closer to router or use Ethernet cable
   ```

2. **Increase timeout in client**
   Edit `~/doorbot/doorbot_client.py`:
   ```python
   # Line ~115, change timeout
   response = requests.get(f"{SERVER_URL}/status", timeout=10)  # increased from 5
   ```

3. **Power supply issues**
   - Use official Raspberry Pi power supply (5V 2.5A minimum)
   - Check if voltage indicator appears on screen

---

## 3️⃣ Raspberry Pi Client Issues

### Problem: Service shows "failed" or "inactive (dead)"

**Symptoms:**
```bash
sudo systemctl status doorbot-client
# Shows: Active: failed (Result: exit-code)
```

**Diagnostics:**
```bash
# View detailed error
sudo journalctl -u doorbot-client -n 50 --no-pager

# Try running manually to see errors
sudo systemctl stop doorbot-client
python3 ~/doorbot/doorbot_client.py
```

**Solutions:**

1. **Python packages missing**
   ```bash
   # Install required packages
   sudo apt-get install python3-rpi.gpio python3-requests

   # Verify
   python3 -c "import RPi.GPIO; import requests; print('OK')"
   ```

2. **Permission denied errors**
   ```bash
   # Add user to GPIO group
   sudo usermod -a -G gpio $USER

   # Reboot to apply
   sudo reboot
   ```

3. **File not found**
   ```bash
   # Verify file exists
   ls -l ~/doorbot/doorbot_client.py

   # Check service file path
   sudo cat /etc/systemd/system/doorbot-client.service

   # Ensure paths match
   ```

4. **Syntax errors in client**
   ```bash
   # Check for Python errors
   python3 -m py_compile ~/doorbot/doorbot_client.py
   ```

### Problem: Client runs but doesn't unlock door

**Symptoms:**
- Service is running
- No errors in logs
- But clicking unlock does nothing

**Diagnostics:**
```bash
# Watch logs in real-time
sudo journalctl -u doorbot-client -f

# In another terminal/browser:
# Click "Unlock Door" button

# Check if client sees the unlock command
```

**Solutions:**

1. **Client not polling frequently enough**
   ```bash
   # Check logs for "Waiting..." messages
   # Should appear every ~1 second

   # If not, check POLL_INTERVAL in client
   ```

2. **Client not receiving letmein=true**
   ```bash
   # Test API directly
   curl http://newyakko.cs.wmich.edu:8878/status

   # Should show: "letmein": false

   # Trigger unlock
   curl -X POST http://newyakko.cs.wmich.edu:8878/unlock

   # Check again
   curl http://newyakko.cs.wmich.edu:8878/status
   # Should show: "letmein": true (briefly)
   ```

3. **Wrong server URL in client**
   ```bash
   # Check client configuration
   grep "SERVER_URL" ~/doorbot/doorbot_client.py

   # Should be: http://newyakko.cs.wmich.edu:8878
   ```

### Problem: Too many consecutive errors

**Symptoms:**
- Client stops with "Too many consecutive errors"

**Solutions:**

1. **Temporary network issue**
   ```bash
   # Just restart the service
   sudo systemctl restart doorbot-client
   ```

2. **Persistent connectivity problem**
   - See Network/Connectivity Issues section above

3. **Increase error threshold**
   Edit `~/doorbot/doorbot_client.py`:
   ```python
   # Line ~137
   max_consecutive_errors = 20  # increased from 10
   ```

---

## 4️⃣ Hardware/GPIO Issues

### Problem: GPIO permission denied

**Symptoms:**
```
RuntimeError: No access to /dev/gpiomem
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Add user to gpio group**
   ```bash
   sudo usermod -a -G gpio pi
   # or
   sudo usermod -a -G gpio Janus

   # Reboot
   sudo reboot
   ```

2. **Run as root (not recommended)**
   ```bash
   # Edit service file
   sudo nano /etc/systemd/system/doorbot-client.service

   # Change: User=root
   # Reload and restart
   sudo systemctl daemon-reload
   sudo systemctl restart doorbot-client
   ```

### Problem: Motor doesn't run

**Symptoms:**
- Unlock command received
- No motor movement
- No errors in logs

**Diagnostics:**
```bash
# Test individual GPIO pins

# Test relay
python3 << 'EOF'
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
print("Turning relay ON")
GPIO.output(4, GPIO.HIGH)
time.sleep(2)
print("Turning relay OFF")
GPIO.output(4, GPIO.LOW)
GPIO.cleanup()
EOF

# Test motor
python3 << 'EOF'
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
pwm = GPIO.PWM(18, 500)
GPIO.output(15, GPIO.HIGH)
print("Starting motor")
pwm.start(50)
time.sleep(2)
pwm.stop()
GPIO.cleanup()
EOF
```

**Solutions:**

1. **Check wiring**
   - Verify GPIO 4 → Relay
   - Verify GPIO 15 → Direction
   - Verify GPIO 18 → Motor PWM
   - Check all connections are secure

2. **Power supply insufficient**
   - Motor needs separate power supply
   - Don't power motor from Pi's GPIO pins
   - Use appropriate relay rated for motor current

3. **Hardware failure**
   - Test relay with multimeter
   - Test motor with direct power connection
   - Replace faulty components

### Problem: Position sensor not working

**Symptoms:**
- Motor runs continuously
- "Position sensor timeout" in logs

**Solutions:**

1. **Check sensor wiring**
   - Verify GPIO 7 connection
   - Check ground connection

2. **Test sensor**
   ```bash
   python3 << 'EOF'
   import RPi.GPIO as GPIO
   import time
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   print("Press the button/sensor...")
   for i in range(50):
       state = GPIO.input(7)
       print(f"State: {state}")
       time.sleep(0.2)
   GPIO.cleanup()
   EOF
   ```

3. **Adjust timeout**
   Edit client to increase timeout if sensor is slow

4. **Disable sensor check** (emergency only)
   - Comment out sensor wait in client
   - Use timed delay instead
   - NOT RECOMMENDED for production

---

## 5️⃣ Service/Startup Issues

### Problem: Service doesn't start on boot

**Symptoms:**
- After reboot, client is not running
- Manual start works fine

**Diagnostics:**
```bash
# Check if service is enabled
sudo systemctl is-enabled doorbot-client

# Check boot logs
sudo journalctl -b -u doorbot-client
```

**Solutions:**

1. **Service not enabled**
   ```bash
   sudo systemctl enable doorbot-client
   ```

2. **Network not ready**
   Service starts before network is up

   Edit `/etc/systemd/system/doorbot-client.service`:
   ```ini
   [Unit]
   After=network-online.target
   Wants=network-online.target

   # Add this:
   [Service]
   ExecStartPre=/bin/sleep 30
   ```

3. **Dependencies not ready**
   ```bash
   # Enable network-online.target
   sudo systemctl enable NetworkManager-wait-online.service
   ```

### Problem: Service keeps restarting

**Symptoms:**
```bash
sudo systemctl status doorbot-client
# Shows: "Restart=always" with many restarts
```

**Solutions:**

1. **Fix underlying error**
   - Check logs for the actual error
   - Fix the root cause
   - See other sections based on error

2. **Increase restart delay**
   Edit service file:
   ```ini
   [Service]
   RestartSec=30  # increased from 10
   ```

3. **Disable auto-restart** (for debugging)
   ```ini
   [Service]
   Restart=no
   ```
   Then start manually to see error

---

## 🔍 Advanced Debugging

### Enable verbose logging

Edit `~/doorbot/doorbot_client.py`, add after imports:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Run client in foreground

```bash
# Stop service
sudo systemctl stop doorbot-client

# Run manually with full output
python3 ~/doorbot/doorbot_client.py
```

### Monitor all GPIO pins

```bash
# Install gpio tools
sudo apt-get install wiringpi

# Monitor pins
watch -n 1 gpio readall
```

### Network packet capture

```bash
# Capture HTTP traffic to server
sudo tcpdump -i any -n port 8878 -A

# In another terminal, trigger unlock
```

### Check system resources

```bash
# CPU and memory usage
top

# Disk space
df -h

# System logs
sudo dmesg | tail -50
```

---

## 📞 Getting Help

### Information to provide when asking for help:

1. **System info:**
   ```bash
   uname -a
   cat /proc/device-tree/model
   python3 --version
   ```

2. **Service status:**
   ```bash
   sudo systemctl status doorbot-client
   ```

3. **Recent logs:**
   ```bash
   sudo journalctl -u doorbot-client -n 100 --no-pager
   ```

4. **Network status:**
   ```bash
   ip addr show
   curl -v http://newyakko.cs.wmich.edu:8878/health
   ```

5. **What you've already tried**

---

## ✅ System Health Checklist

Use this to verify everything is working:

```bash
# Run these commands and check for ✓

# 1. Server is reachable
curl http://newyakko.cs.wmich.edu:8878/health
# ✓ Should return JSON

# 2. Client service is running
sudo systemctl is-active doorbot-client
# ✓ Should output: active

# 3. No recent errors
sudo journalctl -u doorbot-client --since "10 minutes ago" --no-pager | grep -i error
# ✓ Should be empty or minimal

# 4. Network is up
ping -c 1 newyakko.cs.wmich.edu
# ✓ Should show packets received

# 5. GPIO is accessible
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('✓ GPIO OK')"
# ✓ Should print: ✓ GPIO OK
```

**All checks passed? Your system is healthy! 🎉**
