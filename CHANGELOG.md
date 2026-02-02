# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-02-01

### Added
- Initial release - complete replacement for dot.cs.wmich.edu:8878
- Flask server with API compatibility for original system
- Pre-configured Raspberry Pi client for GPIO door control
- Automated SD card preparation script for plug-and-play setup
- Element chatbot integration ($letmein command)
- Web interface for manual door control
- Comprehensive documentation (70+ KB)
  - Quick start guide (3 steps to get working)
  - Complete installation instructions
  - Troubleshooting guide with solutions
  - Manual SD card setup guide
  - Migration guide from dot to newyakko
  - System architecture documentation
- systemd service files for auto-start on boot
- Health check endpoint for monitoring
- Activity logging with timestamps and IP addresses
- GitHub repository with issue templates and PR template
- Contributing guidelines

### Features
- **Server (Flask):**
  - GET / - Returns door status for Pi client polling
  - POST / - Accepts unlock commands from chatbot
  - GET /control - Web interface for manual control
  - GET /health - Server health check
  - Auto-logging of all unlock/lock commands

- **Raspberry Pi Client:**
  - Polls server every 1 second
  - GPIO control for stepper motor and relay
  - Position sensor support
  - Automatic door unlock sequence
  - Error handling and reconnection logic
  - systemd service for auto-start

- **Element Chatbot:**
  - $letmein command integration
  - 3-second unlock window
  - Automatic reset to locked state

- **Setup Tools:**
  - prepare_sd_card.sh - Automated SD card setup
  - install_client.sh - Installation on running Pi
  - setup.sh - Server setup automation
  - test_server.sh - Server API testing

### Documentation
- README.md - Complete project overview
- MIGRATION_FROM_DOT.md - Migration guide
- PROJECT_OVERVIEW.md - System architecture
- raspberry_pi/QUICK_START.md - 3-step setup
- raspberry_pi/INSTALLATION.md - Detailed installation
- raspberry_pi/TROUBLESHOOTING.md - Problem solutions
- raspberry_pi/SD_CARD_MANUAL_SETUP.md - Manual setup
- chatbot_command/README.md - Chatbot integration
- CONTRIBUTING.md - Contribution guidelines

### Technical Details
- Python 3.8+ support
- Flask 2.3+ for web framework
- RPi.GPIO for hardware control
- systemd integration for service management
- NetworkManager for WiFi configuration
- Full API compatibility with original dot server

### Security Notes
- ⚠️ No authentication in v1.0.0
- Suitable for internal networks only
- See documentation for security enhancement options

## [Unreleased]

### Planned Features
- API key authentication
- HTTPS/TLS support
- Rate limiting
- Database logging
- Mobile app integration
- Home Assistant integration
- Multiple door support
- Webhook notifications
- User access control

---

## Release Notes Format

Each release includes:
- **Version number** following semantic versioning
- **Release date**
- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security-related changes

## Migration from dot.cs.wmich.edu

This v1.0.0 release is the initial replacement for the decommissioned dot.cs.wmich.edu:8878 server.

**Key Changes:**
- Server moved from dot.cs.wmich.edu to newyakko.cs.wmich.edu
- API remains 100% compatible
- Enhanced documentation and setup tools
- Added web interface for manual control

See [MIGRATION_FROM_DOT.md](MIGRATION_FROM_DOT.md) for complete migration instructions.
