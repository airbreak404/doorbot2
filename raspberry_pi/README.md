# Raspberry Pi Client Files

**Everything you need to get the Doorbot client running on your Raspberry Pi**

---

## 📁 Files in This Directory

| File | Description |
|------|-------------|
| `doorbot_client.py` | **Main client script** - Pre-configured for newyakko.cs.wmich.edu:8878 |
| `prepare_sd_card.sh` | **Automated SD card setup** - Makes the SD card plug-and-play |
| `install_client.sh` | **Installation script** - Run on the Pi to install everything |
| `QUICK_START.md` | **Quick start guide** - Get up and running in 3 steps |
| `INSTALLATION.md` | **Detailed installation** - Step-by-step manual installation |
| `TROUBLESHOOTING.md` | **Troubleshooting guide** - Solutions to common problems |
| `SD_CARD_MANUAL_SETUP.md` | **Manual SD card setup** - If you prefer to edit files manually |

---

## 🎯 Choose Your Setup Method

### Method 1: Automated SD Card Preparation (Recommended - EASIEST!)

**Best for:** Making the Pi completely plug-and-play

1. Insert your Raspberry Pi SD card into your computer
2. Run the preparation script:
   ```bash
   cd raspberry_pi
   chmod +x prepare_sd_card.sh
   ./prepare_sd_card.sh
   ```
3. Eject SD card, insert into Pi, boot it up
4. **Done!** Client auto-starts

See: [`QUICK_START.md`](QUICK_START.md)

### Method 2: Manual SD Card Setup

**Best for:** Understanding what you're changing

1. Insert SD card into computer
2. Manually copy files and edit configuration
3. See: [`SD_CARD_MANUAL_SETUP.md`](SD_CARD_MANUAL_SETUP.md)

### Method 3: Install After Boot

**Best for:** Pi is already running

1. Copy files to the Pi (USB drive, SCP, or git clone)
2. Run installation script:
   ```bash
   cd raspberry_pi
   chmod +x install_client.sh
   ./install_client.sh
   ```

See: [`INSTALLATION.md`](INSTALLATION.md)

---

## ⚡ Super Quick Start

**Absolute fastest way to get working:**

```bash
# On your computer with SD card inserted:
cd raspberry_pi
./prepare_sd_card.sh

# Follow prompts, then:
# 1. Eject SD card
# 2. Put in Raspberry Pi
# 3. Power on
# 4. Wait 30 seconds
# 5. Done!
```

Test it:
- Open http://newyakko.cs.wmich.edu:8878
- Click "Unlock Door"
- Door unlocks within 1 second ✓

---

## 📋 Pre-Configuration

The client is **pre-configured** with:

- ✅ Server URL: `http://newyakko.cs.wmich.edu:8878`
- ✅ Poll interval: 1 second
- ✅ GPIO pins: 4 (relay), 15 (direction), 18 (PWM), 7 (sensor)
- ✅ PWM frequency: 500 Hz
- ✅ Unlock hold time: 10 seconds
- ✅ Auto-start on boot: Enabled (via systemd)

**No configuration needed!** Just copy and run.

---

## 🔧 If You Need to Change Settings

Edit `doorbot_client.py` (lines 20-40):

```python
# Server Configuration
SERVER_URL = "http://newyakko.cs.wmich.edu:8878"  # Change if server moves
POLL_INTERVAL = 1.0  # How often to check server (seconds)

# GPIO Pin Configuration
RELAY_PIN = 4        # Change if wired differently
DIRECTION_PIN = 15
PWM_PIN = 18
BUTTON_PIN = 7

# Motor Configuration
PWM_FREQUENCY = 500  # Hz
MOTOR_DUTY_CYCLE = 50  # Percent
UNLOCK_HOLD_TIME = 10  # Seconds to hold door unlocked
```

After changing, restart the service:
```bash
sudo systemctl restart doorbot-client
```

---

## 🧪 Testing

### Quick Test (from the Pi):

```bash
# Is server reachable?
curl http://newyakko.cs.wmich.edu:8878/health

# Is client running?
sudo systemctl status doorbot-client

# Any errors?
sudo journalctl -u doorbot-client -n 20
```

### Full System Test:

1. SSH to Pi: `ssh pi@YOUR_PI_IP`
2. Watch logs: `sudo journalctl -u doorbot-client -f`
3. In browser: http://newyakko.cs.wmich.edu:8878
4. Click "Unlock Door"
5. Watch logs show unlock sequence
6. Motor should activate

---

## 🆘 Troubleshooting

**Most common issues:**

### Client won't start
```bash
# Check logs
sudo journalctl -u doorbot-client -n 50

# Install dependencies
sudo apt-get install python3-rpi.gpio python3-requests

# Fix permissions
sudo usermod -a -G gpio $USER
```

### Can't reach server
```bash
# Test connection
ping newyakko.cs.wmich.edu
curl http://newyakko.cs.wmich.edu:8878/health

# Check WiFi
nmcli device status
```

### Motor not running
```bash
# Check GPIO permissions
ls -l /dev/gpiomem

# Test GPIO
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('OK')"

# Check wiring
```

**For complete troubleshooting, see:** [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)

---

## 📚 Documentation Index

Start here based on what you need:

| I want to... | Read this |
|--------------|-----------|
| **Get it working ASAP** | `QUICK_START.md` |
| **Understand how to install** | `INSTALLATION.md` |
| **Prepare the SD card automatically** | Run `prepare_sd_card.sh`, see `QUICK_START.md` |
| **Prepare the SD card manually** | `SD_CARD_MANUAL_SETUP.md` |
| **Fix a problem** | `TROUBLESHOOTING.md` |
| **Understand the system** | `../PROJECT_OVERVIEW.md` |
| **Set up the server** | `../README.md` |

---

## ✅ Success Checklist

Your system is working if:

- [ ] Server accessible at http://newyakko.cs.wmich.edu:8878
- [ ] Pi boots and auto-starts client
- [ ] `sudo systemctl status doorbot-client` shows "active (running)"
- [ ] No errors in logs
- [ ] Clicking "Unlock" triggers motor within 1 second
- [ ] Motor turns handle and holds for 10 seconds
- [ ] Handle returns to locked position
- [ ] Works after reboot

---

## 🎓 How It Works

```
┌─────────────────┐
│  Web Browser    │
│  Click "Unlock" │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Server   │  http://newyakko.cs.wmich.edu:8878
│  Sets letmein   │  /unlock → letmein = true
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pi Client      │  Polls /status every 1 second
│  Checks letmein │  GET /status → {letmein: true/false}
└────────┬────────┘
         │
         ▼ letmein = true
┌─────────────────┐
│  GPIO Control   │  1. Activate relay (GPIO 4)
│  Unlock Door    │  2. Spin motor (GPIO 18, 15)
└─────────────────┘  3. Wait for sensor (GPIO 7)
                     4. Hold 10 seconds
                     5. Return to locked
```

---

## 📦 Requirements

### Hardware
- Raspberry Pi (any model with GPIO)
- Stepper motor
- Relay module
- Position sensor (optional but recommended)
- Proper wiring

### Software
- Raspbian/Raspberry Pi OS
- Python 3.7+
- python3-rpi.gpio
- python3-requests

All software dependencies are automatically installed by the setup scripts.

---

## 🔐 Security Note

**Current implementation has NO authentication.**

Anyone who can reach the server can unlock the door. This is fine for:
- Internal networks
- Testing/development
- Trusted environments

For production, consider:
- Adding API key authentication
- Using HTTPS
- Implementing IP whitelisting
- Adding user accounts

See the main project documentation for security enhancements.

---

## 🚀 Quick Commands

```bash
# Service control
sudo systemctl start doorbot-client
sudo systemctl stop doorbot-client
sudo systemctl restart doorbot-client
sudo systemctl status doorbot-client

# View logs
sudo journalctl -u doorbot-client -f

# Test server
curl http://newyakko.cs.wmich.edu:8878/status

# Run manually
python3 ~/doorbot/doorbot_client.py
```

---

**Ready to get started? See [`QUICK_START.md`](QUICK_START.md)!**
