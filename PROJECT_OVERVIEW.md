# Doorbot2 - Remote Door Lock System

## Project Overview

This project provides a replacement server for a Raspberry Pi-based remote door lock system. The original server (dot.cs.wmich.edu:8878) no longer exists, and this Flask-based server restores full functionality.

## System Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│   Web Interface     │         │  Raspberry Pi Client │
│  (Any Browser)      │────────▶│   (Raspbian)         │
└─────────────────────┘  HTTP   └──────────────────────┘
         │                                │
         │                                │
         ▼                                ▼
┌─────────────────────┐         ┌──────────────────────┐
│   Flask Server      │◀────────│   Polling Every 1s   │
│ newyakko.cs.wmich   │  GET    │   Checks letmein     │
│     Port 8878       │  /status│                      │
└─────────────────────┘         └──────────────────────┘
         │                                │
         │                                ▼
         │                       ┌──────────────────────┐
         │                       │  GPIO Control        │
         │                       │  - Stepper Motor     │
         │                       │  - Relay             │
         │                       │  - Position Sensor   │
         │                       └──────────────────────┘
         │                                │
         │                                ▼
         │                       ┌──────────────────────┐
         └──────────────────────▶│   Door Handle        │
                POST /unlock     │   Physical Unlock    │
                                 └──────────────────────┘
```

## Hardware Components

### Raspberry Pi Setup
- **Model**: Raspberry Pi (Raspbian Bookworm)
- **Stepper Motor**: Rotates door handle to unlock position
- **Relay Module**: Controls motor power
- **Position Sensor**: Detects unlock position reached

### GPIO Pin Assignment
| GPIO Pin | Function |
|----------|----------|
| GPIO 4   | Power relay control |
| GPIO 15  | Motor direction control |
| GPIO 18  | Stepper motor PWM |
| GPIO 7   | Handle position sensor |

## Software Components

### Server (This Repository)
- **Technology**: Python Flask
- **Host**: newyakko.cs.wmich.edu
- **Port**: 8878
- **Features**:
  - Web-based control panel
  - REST API for client polling
  - Auto-reset safety (15s timeout)
  - Activity logging
  - Health monitoring

### Raspberry Pi Client
- **Location**: `/home/Janus/Downloads/doorbot_client.py`
- **Behavior**: Polls server every 1 second
- **Action**: Executes unlock sequence when `letmein=true`

## API Specification

### GET /status
Returns current lock state (polled by Pi client)

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

### POST /lock
Manually resets lock state

### GET /health
Health check endpoint

## Quick Start

### Server Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/doorbot2.git
cd doorbot2

# Install dependencies
pip3 install -r requirements.txt

# Run the server
python3 server.py
```

Access at: http://newyakko.cs.wmich.edu:8878

### Raspberry Pi Configuration

1. Update client URL in `/home/Janus/Downloads/doorbot_client.py` (line 49):
```python
server_url = "http://newyakko.cs.wmich.edu:8878"
```

2. Set up auto-start via systemd (see [RASPBERRY_PI_SETUP.md](RASPBERRY_PI_SETUP.md))

## Files in This Repository

| File | Description |
|------|-------------|
| `server.py` | Main Flask server application |
| `requirements.txt` | Python dependencies |
| `README.md` | Installation and usage guide |
| `RASPBERRY_PI_SETUP.md` | Raspberry Pi configuration guide |
| `doorbot-server.service` | systemd service file |
| `setup.sh` | Automated setup script |
| `test_server.sh` | Server testing script |
| `PROJECT_OVERVIEW.md` | This file - project documentation |

## Security Considerations

**⚠️ Current Implementation**: No authentication

The current implementation has **no authentication**. Anyone who can access the URL can unlock the door. This is fine for internal networks but not suitable for internet-facing deployments.

**For production use**, consider:
- API key authentication
- HTTPS/TLS encryption
- IP whitelisting
- Rate limiting
- User authentication system

## Deployment

### Development/Testing
```bash
python3 server.py
```

### Production (systemd service)
```bash
sudo cp doorbot-server.service /etc/systemd/system/
sudo systemctl enable doorbot-server
sudo systemctl start doorbot-server
```

### Monitoring
```bash
# Check service status
sudo systemctl status doorbot-server

# View logs
sudo journalctl -u doorbot-server -f
```

## Troubleshooting

### Server Issues
- **Port already in use**: Check with `sudo lsof -i :8878`
- **Flask not installed**: Run `pip3 install flask`
- **Firewall blocking**: Open port 8878

### Client Issues
- **Can't connect**: Test with `curl http://newyakko.cs.wmich.edu:8878/health`
- **Motor not running**: Check GPIO permissions and wiring
- **WiFi issues**: Verify connection to "morgana" network

See [README.md](README.md) for detailed troubleshooting.

## Testing

```bash
# Run automated tests
./test_server.sh

# Manual API testing
curl http://newyakko.cs.wmich.edu:8878/status
curl -X POST http://newyakko.cs.wmich.edu:8878/unlock
```

## Project History

- **Original Server**: dot.cs.wmich.edu:8878 (Western Michigan University - no longer exists)
- **New Server**: newyakko.cs.wmich.edu:8878 (This implementation)
- **Client**: Unchanged (only server URL updated)

## License

This is a restoration/replacement project for an existing system. Use at your own discretion.

## Contributing

Improvements welcome! Areas for enhancement:
- Authentication system
- HTTPS support
- Mobile app integration
- Database logging
- Multiple door support
- Access control lists

## Support

For issues or questions:
1. Check the [README.md](README.md)
2. Review [RASPBERRY_PI_SETUP.md](RASPBERRY_PI_SETUP.md)
3. Open a GitHub issue

## Acknowledgments

Original system design and Raspberry Pi client by Western Michigan University CS Department.
Server replacement and documentation by the Doorbot2 project.
