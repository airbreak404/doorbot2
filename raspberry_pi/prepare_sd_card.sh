#!/bin/bash

# Raspberry Pi SD Card Preparation Script
# This script configures the SD card for plug-and-play operation
# Run this on your computer with the SD card mounted

set -e

echo "=============================================="
echo "🚪 Doorbot SD Card Preparation"
echo "=============================================="
echo ""
echo "This script will configure your Raspberry Pi SD card"
echo "for plug-and-play operation. No configuration needed"
echo "after inserting the SD card into the Pi."
echo ""

# Detect SD card mount point
echo "Step 1: Detecting SD card..."
echo "----------------------------------------------"

# Common mount points
POSSIBLE_MOUNTS=(
    "/media/$USER/rootfs"
    "/media/$USER/boot"
    "/Volumes/boot"
    "/Volumes/rootfs"
    "/mnt/rootfs"
    "/mnt/boot"
)

BOOT_MOUNT=""
ROOT_MOUNT=""

for mount in "${POSSIBLE_MOUNTS[@]}"; do
    if [ -d "$mount" ]; then
        if [[ "$mount" == *"boot"* ]]; then
            BOOT_MOUNT="$mount"
            echo "✓ Found boot partition: $BOOT_MOUNT"
        elif [[ "$mount" == *"root"* ]]; then
            ROOT_MOUNT="$mount"
            echo "✓ Found root partition: $ROOT_MOUNT"
        fi
    fi
done

# Manual selection if not found
if [ -z "$ROOT_MOUNT" ]; then
    echo ""
    echo "Could not auto-detect SD card."
    echo "Please enter the root filesystem mount point manually."
    echo "Examples: /media/$USER/rootfs, /Volumes/rootfs"
    read -p "Root mount point: " ROOT_MOUNT

    if [ ! -d "$ROOT_MOUNT" ]; then
        echo "❌ Error: Directory $ROOT_MOUNT does not exist"
        exit 1
    fi
fi

if [ -z "$BOOT_MOUNT" ]; then
    echo "Please enter the boot partition mount point."
    echo "Examples: /media/$USER/boot, /Volumes/boot"
    read -p "Boot mount point (or press Enter to skip): " BOOT_MOUNT
fi

echo ""
echo "Using:"
echo "  Root: $ROOT_MOUNT"
if [ -n "$BOOT_MOUNT" ]; then
    echo "  Boot: $BOOT_MOUNT"
fi
echo ""

# Verify this looks like a Raspberry Pi SD card
if [ ! -d "$ROOT_MOUNT/etc" ] || [ ! -d "$ROOT_MOUNT/home" ]; then
    echo "⚠️  Warning: This doesn't look like a Raspberry Pi root filesystem"
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Determine the user (usually 'pi' or 'Janus')
echo "Step 2: Detecting Raspberry Pi user..."
echo "----------------------------------------------"

if [ -d "$ROOT_MOUNT/home/Janus" ]; then
    PI_USER="Janus"
    echo "✓ Found user: Janus"
elif [ -d "$ROOT_MOUNT/home/pi" ]; then
    PI_USER="pi"
    echo "✓ Found user: pi"
else
    echo "Could not detect user. Please enter username:"
    read -p "Username: " PI_USER

    if [ ! -d "$ROOT_MOUNT/home/$PI_USER" ]; then
        echo "Creating /home/$PI_USER..."
        sudo mkdir -p "$ROOT_MOUNT/home/$PI_USER"
    fi
fi

USER_HOME="$ROOT_MOUNT/home/$PI_USER"
echo "Home directory: $USER_HOME"
echo ""

# Create installation directory
echo "Step 3: Installing doorbot client..."
echo "----------------------------------------------"

INSTALL_DIR="$USER_HOME/doorbot"
sudo mkdir -p "$INSTALL_DIR"

# Copy client script
if [ ! -f "doorbot_client.py" ]; then
    echo "❌ Error: doorbot_client.py not found in current directory"
    echo "Please run this script from the raspberry_pi folder"
    exit 1
fi

echo "Copying doorbot_client.py..."
sudo cp doorbot_client.py "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/doorbot_client.py"
echo "✓ Client installed to: /home/$PI_USER/doorbot/doorbot_client.py"

# Set ownership
sudo chown -R 1000:1000 "$INSTALL_DIR"  # UID/GID for pi/Janus user

echo ""

# Create systemd service
echo "Step 4: Creating systemd service..."
echo "----------------------------------------------"

SERVICE_DIR="$ROOT_MOUNT/etc/systemd/system"
sudo mkdir -p "$SERVICE_DIR"

SERVICE_FILE="$SERVICE_DIR/doorbot-client.service"

echo "Creating service file..."
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Doorbot Client - Door Lock Controller
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$PI_USER
WorkingDirectory=/home/$PI_USER/doorbot
ExecStart=/usr/bin/python3 /home/$PI_USER/doorbot/doorbot_client.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Service file created"

# Enable the service
echo "Enabling service for auto-start..."
SYMLINK_DIR="$ROOT_MOUNT/etc/systemd/system/multi-user.target.wants"
sudo mkdir -p "$SYMLINK_DIR"
sudo ln -sf /etc/systemd/system/doorbot-client.service "$SYMLINK_DIR/doorbot-client.service"
echo "✓ Service enabled"

echo ""

# Configure WiFi (if WiFi credentials are found)
echo "Step 5: Checking WiFi configuration..."
echo "----------------------------------------------"

WIFI_CONFIG="$ROOT_MOUNT/etc/NetworkManager/system-connections/preconfigured.nmconnection"

if [ -f "$WIFI_CONFIG" ]; then
    echo "✓ WiFi config found: $WIFI_CONFIG"
    echo "  Current SSID: $(sudo grep -Po 'ssid=\K.*' $WIFI_CONFIG || echo 'unknown')"

    echo "WiFi is already configured. Modify settings? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        read -p "Enter WiFi SSID: " WIFI_SSID
        read -sp "Enter WiFi Password: " WIFI_PASSWORD
        echo ""

        sudo tee "$WIFI_CONFIG" > /dev/null <<EOF
[connection]
id=preconfigured
uuid=$(uuidgen)
type=wifi
autoconnect=true

[wifi]
mode=infrastructure
ssid=$WIFI_SSID

[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=$WIFI_PASSWORD

[ipv4]
method=auto

[ipv6]
addr-gen-mode=stable-privacy
method=auto
EOF

        sudo chmod 600 "$WIFI_CONFIG"
        echo "✓ WiFi configured for SSID: $WIFI_SSID"
    fi
else
    echo "⚠️  No existing WiFi configuration found"
    echo "Configure WiFi now? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        read -p "Enter WiFi SSID: " WIFI_SSID
        read -sp "Enter WiFi Password: " WIFI_PASSWORD
        echo ""

        sudo mkdir -p "$ROOT_MOUNT/etc/NetworkManager/system-connections"

        sudo tee "$WIFI_CONFIG" > /dev/null <<EOF
[connection]
id=preconfigured
uuid=$(uuidgen)
type=wifi
autoconnect=true

[wifi]
mode=infrastructure
ssid=$WIFI_SSID

[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=$WIFI_PASSWORD

[ipv4]
method=auto

[ipv6]
addr-gen-mode=stable-privacy
method=auto
EOF

        sudo chmod 600 "$WIFI_CONFIG"
        echo "✓ WiFi configured for SSID: $WIFI_SSID"
    else
        echo "⚠️  Skipping WiFi configuration"
        echo "   You'll need to configure WiFi manually after boot"
    fi
fi

echo ""

# Create README on desktop
echo "Step 6: Creating helpful files..."
echo "----------------------------------------------"

DESKTOP_DIR="$USER_HOME/Desktop"
sudo mkdir -p "$DESKTOP_DIR"

sudo tee "$DESKTOP_DIR/DOORBOT_README.txt" > /dev/null <<EOF
==============================================
🚪 DOORBOT CLIENT - QUICK REFERENCE
==============================================

Your Raspberry Pi is configured and ready!

SERVER: http://newyakko.cs.wmich.edu:8878

The doorbot client is running automatically in the background.

USEFUL COMMANDS:
---------------

# Check if client is running
sudo systemctl status doorbot-client

# View live logs
sudo journalctl -u doorbot-client -f

# Restart the client
sudo systemctl restart doorbot-client

# Stop the client
sudo systemctl stop doorbot-client

# Test server connection
curl http://newyakko.cs.wmich.edu:8878/status


TESTING:
--------

1. Open http://newyakko.cs.wmich.edu:8878 in a browser
2. Click "Unlock Door"
3. Watch the logs: sudo journalctl -u doorbot-client -f
4. Motor should activate within 1 second


CONFIGURATION:
--------------

Client location: /home/$PI_USER/doorbot/doorbot_client.py
Service file: /etc/systemd/system/doorbot-client.service

To change settings, edit the client file and restart:
  nano ~/doorbot/doorbot_client.py
  sudo systemctl restart doorbot-client


TROUBLESHOOTING:
----------------

If the client isn't working:

1. Check service status:
   sudo systemctl status doorbot-client

2. Check logs for errors:
   sudo journalctl -u doorbot-client -n 50

3. Test server manually:
   curl http://newyakko.cs.wmich.edu:8878/health

4. Verify WiFi connection:
   ping newyakko.cs.wmich.edu

5. Run client manually for debugging:
   sudo systemctl stop doorbot-client
   python3 ~/doorbot/doorbot_client.py


For more help, see the GitHub repository.

==============================================
EOF

sudo chown 1000:1000 "$DESKTOP_DIR/DOORBOT_README.txt"

echo "✓ Created Desktop/DOORBOT_README.txt"

echo ""

# Summary
echo "=============================================="
echo "✅ SD Card Preparation Complete!"
echo "=============================================="
echo ""
echo "Configuration Summary:"
echo "  • Client installed: /home/$PI_USER/doorbot/"
echo "  • Service enabled: doorbot-client.service"
echo "  • Auto-start: YES"
echo "  • Server: http://newyakko.cs.wmich.edu:8878"
echo ""
echo "Next Steps:"
echo "  1. Safely eject the SD card"
echo "  2. Insert into Raspberry Pi"
echo "  3. Power on the Pi"
echo "  4. Wait ~30 seconds for boot"
echo "  5. Client will start automatically!"
echo ""
echo "To test:"
echo "  • Open: http://newyakko.cs.wmich.edu:8878"
echo "  • Click 'Unlock Door'"
echo "  • Door should unlock within 1 second"
echo ""
echo "The Pi will have a README on the desktop with"
echo "all commands and troubleshooting info."
echo ""
echo "=============================================="
echo ""
