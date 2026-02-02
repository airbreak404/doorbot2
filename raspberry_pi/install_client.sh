#!/bin/bash

# Doorbot Client Installation Script for Raspberry Pi
# This script installs and configures the doorbot client

set -e  # Exit on error

echo "======================================"
echo "🚪 Doorbot Client Installation"
echo "======================================"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ] || ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if running as correct user
CURRENT_USER=$(whoami)
echo "Current user: $CURRENT_USER"
echo "Installation will be for user: $CURRENT_USER"
echo ""

# Install dependencies
echo "Step 1: Installing dependencies..."
echo "--------------------------------------"

# Update package list
echo "Updating package list..."
sudo apt-get update -qq

# Install Python3 and pip if not present
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    sudo apt-get install -y python3
else
    echo "✓ Python 3 already installed: $(python3 --version)"
fi

if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo apt-get install -y python3-pip
else
    echo "✓ pip3 already installed"
fi

# Install required Python packages
echo "Installing Python packages..."
sudo apt-get install -y python3-rpi.gpio python3-requests

echo "✓ Dependencies installed"
echo ""

# Create installation directory
echo "Step 2: Installing client script..."
echo "--------------------------------------"

INSTALL_DIR="/home/$CURRENT_USER/doorbot"
mkdir -p "$INSTALL_DIR"

# Copy client script
if [ -f "doorbot_client.py" ]; then
    cp doorbot_client.py "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/doorbot_client.py"
    echo "✓ Client installed to: $INSTALL_DIR/doorbot_client.py"
else
    echo "❌ Error: doorbot_client.py not found in current directory"
    exit 1
fi

echo ""

# Test server connectivity
echo "Step 3: Testing server connectivity..."
echo "--------------------------------------"

SERVER_URL="http://newyakko.cs.wmich.edu:8878"
if curl -s --connect-timeout 5 "$SERVER_URL/health" > /dev/null 2>&1; then
    echo "✓ Server is reachable: $SERVER_URL"
else
    echo "⚠️  Warning: Cannot reach server at $SERVER_URL"
    echo "   The server may not be running yet, or network is not configured."
    echo "   Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Set up systemd service
echo "Step 4: Setting up systemd service..."
echo "--------------------------------------"

SERVICE_FILE="/etc/systemd/system/doorbot-client.service"

echo "Creating service file: $SERVICE_FILE"

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Doorbot Client - Door Lock Controller
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/doorbot_client.py
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

# Reload systemd
sudo systemctl daemon-reload

# Enable service
echo "Enabling service to start on boot..."
sudo systemctl enable doorbot-client.service

echo "✓ Service enabled"
echo ""

# Ask if user wants to start now
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Installation directory: $INSTALL_DIR"
echo "Service name: doorbot-client.service"
echo "Server URL: $SERVER_URL"
echo ""
echo "Would you like to start the client now? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting doorbot-client service..."
    sudo systemctl start doorbot-client.service

    echo ""
    echo "Waiting 2 seconds for service to start..."
    sleep 2

    echo ""
    echo "Service Status:"
    echo "--------------------------------------"
    sudo systemctl status doorbot-client.service --no-pager -l

    echo ""
    echo "Recent Logs:"
    echo "--------------------------------------"
    sudo journalctl -u doorbot-client.service -n 20 --no-pager
fi

echo ""
echo "======================================"
echo "Useful Commands:"
echo "======================================"
echo ""
echo "# Start the service"
echo "sudo systemctl start doorbot-client"
echo ""
echo "# Stop the service"
echo "sudo systemctl stop doorbot-client"
echo ""
echo "# Restart the service"
echo "sudo systemctl restart doorbot-client"
echo ""
echo "# Check service status"
echo "sudo systemctl status doorbot-client"
echo ""
echo "# View live logs"
echo "sudo journalctl -u doorbot-client -f"
echo ""
echo "# Run manually (for testing)"
echo "python3 $INSTALL_DIR/doorbot_client.py"
echo ""
echo "======================================"
echo ""
