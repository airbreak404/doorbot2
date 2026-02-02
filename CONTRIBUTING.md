# Contributing to Doorbot2

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional environment

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/doorbot2.git
   cd doorbot2
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check the [Troubleshooting Guide](raspberry_pi/TROUBLESHOOTING.md)
2. Search existing issues to avoid duplicates
3. Gather system information and logs

When reporting bugs, include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs
- System information (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
1. Check if the feature already exists or is planned
2. Clearly describe the use case
3. Explain how it would benefit users
4. Consider implementation challenges

### Areas for Contribution

We especially welcome contributions in these areas:

**Security Enhancements:**
- API key authentication
- HTTPS/TLS support
- Rate limiting
- Access control lists

**Features:**
- Mobile app integration
- Database logging
- Webhook notifications
- Home Assistant integration
- Multiple door support

**Documentation:**
- Additional examples
- Video tutorials
- Translations
- Improved troubleshooting

**Testing:**
- Unit tests
- Integration tests
- Hardware test fixtures

## Development Setup

### Server Development

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run in development mode
python3 server.py

# Test the API
curl http://localhost:8878/health
```

### Raspberry Pi Client Development

```bash
# On the Raspberry Pi
cd raspberry_pi

# Install dependencies
sudo apt-get install python3-rpi.gpio python3-requests

# Test the client (requires hardware)
python3 doorbot_client.py
```

### Development Environment

Recommended tools:
- Python 3.8 or later
- Virtual environment for isolation
- Code editor with Python support (VS Code, PyCharm, etc.)
- Git for version control

## Testing

### Manual Testing

**Server:**
```bash
# Test health endpoint
curl http://localhost:8878/health

# Test GET endpoint (Pi polling)
curl http://localhost:8878/

# Test POST endpoint (chatbot)
curl -X POST http://localhost:8878/ \
  -H "Content-Type: application/json" \
  -d '{"status": {"letmein": true}}'
```

**Client (requires Raspberry Pi):**
```bash
# Run manually and watch output
python3 doorbot_client.py

# Check for errors
# Verify GPIO initialization
# Test unlock sequence
```

### Automated Testing

We currently don't have automated tests, but contributions are welcome!

Potential test coverage:
- Server API endpoints
- Client state management
- Error handling
- GPIO control (with mocks)

## Documentation

### Documentation Standards

- Use clear, concise language
- Include code examples
- Add screenshots where helpful
- Keep guides up-to-date with code changes
- Use proper Markdown formatting

### Documentation Structure

```
doorbot2/
├── README.md                      # Main project overview
├── MIGRATION_FROM_DOT.md          # Migration guide
├── PROJECT_OVERVIEW.md            # System architecture
├── CONTRIBUTING.md                # This file
├── raspberry_pi/
│   ├── README.md                  # Client overview
│   ├── QUICK_START.md             # Quick start guide
│   ├── INSTALLATION.md            # Detailed setup
│   ├── TROUBLESHOOTING.md         # Problem solutions
│   └── SD_CARD_MANUAL_SETUP.md   # Manual setup
└── chatbot_command/
    └── README.md                  # Chatbot integration
```

When adding features, update relevant documentation.

## Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
Add authentication to server API

- Implement API key validation
- Add middleware for protected endpoints
- Update documentation with auth examples
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description with bullet points
- Reference issues if applicable

### Pull Request Process

1. **Update your branch** with latest main:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes** thoroughly

3. **Update documentation** as needed

4. **Create a pull request** on GitHub:
   - Use the PR template
   - Describe your changes clearly
   - Reference any related issues
   - Include test results

5. **Respond to feedback** from reviewers

6. **Wait for approval** and merge

### Review Process

Pull requests will be reviewed for:
- Code quality and style
- Functionality and correctness
- Documentation completeness
- Test coverage
- Breaking changes
- Security implications

## Code Style

### Python Style

Follow PEP 8 guidelines:
- 4 spaces for indentation (no tabs)
- Max line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions
- Comment complex logic

Example:
```python
def unlock_door(duration: int) -> bool:
    """
    Unlock the door for specified duration

    Args:
        duration: Time in seconds to hold door unlocked

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Activate GPIO relay
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        return True
    except Exception as e:
        logger.error(f"Unlock failed: {e}")
        return False
```

### File Organization

- Keep files focused and single-purpose
- Use clear, descriptive filenames
- Group related functionality
- Avoid large monolithic files

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the question label
4. Ask in discussions (if available)

## Recognition

Contributors will be recognized in:
- README credits
- Release notes
- Commit history

Thank you for contributing to Doorbot2! 🚪✨
