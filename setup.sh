#!/bin/bash

# Doorbot Server Setup Script
# Run this script to set up the server on newyakko.cs.wmich.edu

echo "======================================"
echo "🚪 Doorbot Server Setup"
echo "======================================"

# Check if running on the correct server
echo ""
echo "Step 1: Checking environment..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

# Install Flask
echo ""
echo "Step 2: Installing Flask..."
if python3 -c "import flask" 2>/dev/null; then
    FLASK_VERSION=$(python3 -c "import flask; print(flask.__version__)")
    echo "✓ Flask already installed: $FLASK_VERSION"
else
    echo "Installing Flask..."
    pip3 install --user flask
    if [ $? -eq 0 ]; then
        echo "✓ Flask installed successfully"
    else
        echo "✗ Failed to install Flask"
        exit 1
    fi
fi

# Test the server
echo ""
echo "Step 3: Testing server..."
echo "Starting server in test mode (will run for 5 seconds)..."
timeout 5 python3 server.py &
sleep 2

if curl -s http://localhost:8878/health > /dev/null; then
    echo "✓ Server test successful"
else
    echo "✗ Server test failed"
fi

# Offer to set up systemd service
echo ""
echo "Step 4: Service installation"
echo "Would you like to install the systemd service? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Installing systemd service..."
    sudo cp doorbot-server.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable doorbot-server.service
    echo "✓ Service installed"
    echo ""
    echo "Start the service with: sudo systemctl start doorbot-server"
    echo "Check status with: sudo systemctl status doorbot-server"
else
    echo "Skipped service installation"
    echo "You can run the server manually with: python3 server.py"
fi

# Summary
echo ""
echo "======================================"
echo "✓ Setup Complete!"
echo "======================================"
echo "Server location: $(pwd)"
echo "Web interface: http://newyakko.cs.wmich.edu:8878"
echo "API endpoint: http://newyakko.cs.wmich.edu:8878/status"
echo ""
echo "Next steps:"
echo "1. Start the server (manually or via systemd)"
echo "2. Update Raspberry Pi client to point to:"
echo "   http://newyakko.cs.wmich.edu:8878"
echo "3. Open firewall port 8878 if needed"
echo ""
