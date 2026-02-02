---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''

---

## Bug Description
A clear and concise description of what the bug is.

## Component Affected
- [ ] Server (Flask application)
- [ ] Raspberry Pi Client
- [ ] Element Chatbot Command
- [ ] Documentation
- [ ] Other (please specify)

## Steps To Reproduce
1. Go to '...'
2. Run command '....'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Error Messages
```
Paste any error messages here
```

## System Information
**Server:**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.10.0]
- Flask Version: [e.g., 2.3.0]

**Raspberry Pi (if applicable):**
- Model: [e.g., Raspberry Pi 4]
- OS: [e.g., Raspbian Bookworm]
- Python Version: [e.g., 3.11.0]

## Logs
**Server logs:**
```
sudo journalctl -u doorbot-server -n 50
```

**Pi client logs (if applicable):**
```
sudo journalctl -u doorbot-client -n 50
```

## Additional Context
Add any other context about the problem here.

## Have You Checked?
- [ ] [Troubleshooting Guide](../../raspberry_pi/TROUBLESHOOTING.md)
- [ ] Server is running and accessible
- [ ] Firewall allows port 8878
- [ ] All URLs point to correct server
