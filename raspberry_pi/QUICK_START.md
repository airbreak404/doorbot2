# 🚀 Doorbot Quick Start Guide

**Get your door lock working in 3 simple steps!**

---

## ⚡ Super Quick Setup (Plug and Play)

### You Will Need:
- ✅ Raspberry Pi SD card
- ✅ Computer with SD card reader
- ✅ Server running at newyakko.cs.wmich.edu:8878

### Step 1: Prepare the SD Card (One-Time Setup)

**Insert the Raspberry Pi SD card into your computer**

```bash
# Clone or download this repository
cd doorbot2/raspberry_pi

# Run the preparation script
chmod +x prepare_sd_card.sh
./prepare_sd_card.sh
```

The script will:
- ✓ Detect your SD card automatically
- ✓ Install the doorbot client
- ✓ Configure auto-start service
- ✓ Set up WiFi (if needed)
- ✓ Create helpful reference files

### Step 2: Insert SD Card and Boot

1. Safely eject the SD card from your computer
2. Insert it into the Raspberry Pi
3. Connect power to the Pi
4. Wait ~30 seconds for it to boot

**That's it! The client is now running automatically.**

### Step 3: Test It!

1. Open a web browser
2. Go to: **http://newyakko.cs.wmich.edu:8878**
3. Click "Unlock Door"
4. Within 1 second, the door should unlock

---

## 🔍 Verify It's Working

### Check #1: Is the server running?

Open in browser: http://newyakko.cs.wmich.edu:8878

You should see the Doorbot Control Panel.

### Check #2: Is the Pi connected?

SSH into your Pi:
```bash
ssh pi@YOUR_PI_IP  # or ssh Janus@YOUR_PI_IP
```

Check the client status:
```bash
sudo systemctl status doorbot-client
```

Should show: **Active: active (running)**

### Check #3: Are there any errors?

View the logs:
```bash
sudo journalctl -u doorbot-client -f
```

You should see:
```
🚪 DOORBOT CLIENT
Server: http://newyakko.cs.wmich.edu:8878
Initializing GPIO pins...
Starting server polling...
```

No error messages!

---

## 🎯 Testing the Complete System

### Full Test Procedure:

1. **SSH into the Pi and start watching logs:**
   ```bash
   sudo journalctl -u doorbot-client -f
   ```

2. **Open the web interface in a browser:**
   http://newyakko.cs.wmich.edu:8878

3. **Click "Unlock Door" button**

4. **Watch the logs - within 1 second you should see:**
   ```
   🔓 UNLOCKING DOOR
   Activating power relay...
   Starting motor (unlock direction)...
   Waiting for unlock position...
   ✓ Unlock position reached!
   Holding unlocked for 10 seconds...
   Returning to locked position...
   ✓ Door lock sequence complete
   ```

5. **Physical check:**
   - Motor should spin
   - Door handle should turn
   - After 10 seconds, handle returns to locked position

**If all of this works: ✅ Your system is fully operational!**

---

## 📍 Quick Command Reference

### On the Raspberry Pi:

```bash
# Check if client is running
sudo systemctl status doorbot-client

# View live logs
sudo journalctl -u doorbot-client -f

# Restart client
sudo systemctl restart doorbot-client

# Stop client
sudo systemctl stop doorbot-client

# Start client
sudo systemctl start doorbot-client
```

### From Any Computer:

```bash
# Test server connection
curl http://newyakko.cs.wmich.edu:8878/status

# Expected response:
# {"letmein": false, "last_command_time": null, ...}

# Trigger unlock from command line
curl -X POST http://newyakko.cs.wmich.edu:8878/unlock
```

---

## ❌ Something Not Working?

### Problem: Can't access the web interface

**Solution:**
1. Verify server is running:
   ```bash
   curl http://newyakko.cs.wmich.edu:8878/health
   ```
2. Check if server is up on newyakko.cs.wmich.edu
3. Make sure port 8878 is not blocked by firewall

### Problem: Pi client shows "Cannot connect to server"

**Solution:**
1. Check Pi's network connection:
   ```bash
   ping newyakko.cs.wmich.edu
   ```
2. Verify WiFi is connected:
   ```bash
   nmcli device status
   ```
3. Test server from Pi:
   ```bash
   curl http://newyakko.cs.wmich.edu:8878/health
   ```

### Problem: Motor not running when unlock is triggered

**Solution:**
1. Check client logs for GPIO errors:
   ```bash
   sudo journalctl -u doorbot-client -n 50
   ```
2. Verify user has GPIO permissions:
   ```bash
   sudo usermod -a -G gpio $USER
   ```
3. Test hardware separately:
   ```bash
   # If you have test scripts
   python3 ~/Downloads/Relaytest.py
   python3 ~/Downloads/steppertest.py
   ```
4. Check wiring connections

### Problem: Service won't start

**Solution:**
1. Check service status:
   ```bash
   sudo systemctl status doorbot-client
   ```
2. Look for error messages
3. Try running manually:
   ```bash
   python3 ~/doorbot/doorbot_client.py
   ```
4. Check if Python packages are installed:
   ```bash
   python3 -c "import RPi.GPIO; import requests"
   ```

---

## 📚 Need More Help?

- **Detailed troubleshooting:** See `TROUBLESHOOTING.md`
- **Installation details:** See `INSTALLATION.md`
- **System architecture:** See `../PROJECT_OVERVIEW.md`
- **Server setup:** See `../README.md`

---

## 🎉 Success Checklist

Before considering the system complete, verify:

- [ ] Server accessible at http://newyakko.cs.wmich.edu:8878
- [ ] Web interface loads and shows status
- [ ] Raspberry Pi boots and connects to network
- [ ] Client service shows "active (running)"
- [ ] Logs show no errors
- [ ] Clicking "Unlock" triggers unlock sequence within 1 second
- [ ] Motor activates and turns handle
- [ ] Position sensor detected (if installed)
- [ ] Handle returns to locked position after timeout
- [ ] System works reliably on reboot

**All checked? Congratulations! Your Doorbot system is fully operational! 🎊**
