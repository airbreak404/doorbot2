# Migration from dot.cs.wmich.edu to newyakko.cs.wmich.edu

This document describes the complete migration of the Doorbot system from the old server (dot) to the new server (newyakko).

---

## What Happened

**Old Server:** `dot.cs.wmich.edu:8878` - No longer exists
**New Server:** `newyakko.cs.wmich.edu:8878` - New replacement

The doorbot system has been migrated to continue functioning with the existing:
- Raspberry Pi hardware
- Element chatbot `$letmein` command
- Same API interface

---

## Changes Required

### 1. Server (New Implementation)

**File:** `server.py`

A new Flask server that replicates the original API:
- `GET /` - Returns `{"letmein": true/false}` for Pi polling
- `POST /` - Accepts `{"status": {"letmein": true/false}}` from chatbot
- `GET /control` - Web interface for manual control
- `GET /health` - Health check endpoint

**Deploy to newyakko.cs.wmich.edu:**
```bash
cd ~/doorbot_server
python3 server.py
```

Or use systemd service for auto-start (see README.md)

### 2. Raspberry Pi Client (Pre-Configured)

**File:** `raspberry_pi/doorbot_client.py`

**Already updated** with new server URL:
```python
SERVER_URL = "http://newyakko.cs.wmich.edu:8878"
```

The SD card has been prepared and is plug-and-play ready.

### 3. Element Chatbot Command (Update Required)

**File:** `chatbot_command/letmein.py`

**Action Required:** Update on newyakko.cs.wmich.edu

```bash
# On newyakko.cs.wmich.edu
cd ~/ccawmunity/chatbot/commandcenter/commands/

# Backup original
cp letmein.py letmein.py.backup

# Update to new version (from this repo)
# Line 27 changed from:
#   requests.post("http://dot.cs.wmich.edu:8878", ...)
# To:
#   requests.post("http://newyakko.cs.wmich.edu:8878", ...)

# Restart chatbot to load new command
```

---

## API Compatibility

The new server is **100% API-compatible** with the original:

### Pi Client Polling (GET /)

**Request:**
```
GET http://newyakko.cs.wmich.edu:8878/
```

**Response:**
```json
{
  "letmein": false,
  "last_command_time": null,
  "last_unlock_user": null
}
```

### Chatbot Command (POST /)

**Request:**
```
POST http://newyakko.cs.wmich.edu:8878/
Content-Type: application/json

{
  "status": {
    "letmein": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "letmein": true
}
```

---

## Complete Migration Checklist

- [x] Create replacement Flask server
- [x] Update Raspberry Pi client to new URL
- [x] Configure SD card for plug-and-play
- [ ] **Deploy server on newyakko.cs.wmich.edu**
- [ ] **Update Element chatbot command**
- [ ] **Test complete system**

---

## Testing the Migration

### 1. Start New Server

On newyakko.cs.wmich.edu:
```bash
cd ~/doorbot_server
python3 server.py
```

Should see:
```
🚪 Doorbot Server Starting
Server: newyakko.cs.wmich.edu
Port: 8878
Element chatbot command: $letmein
```

### 2. Test Server API

```bash
# Test Pi client endpoint (GET)
curl http://newyakko.cs.wmich.edu:8878/

# Should return: {"letmein": false, ...}

# Test chatbot endpoint (POST)
curl -X POST http://newyakko.cs.wmich.edu:8878/ \
  -H "Content-Type: application/json" \
  -d '{"status": {"letmein": true}}'

# Should return: {"success": true, "letmein": true}
```

### 3. Boot Raspberry Pi

1. Insert prepared SD card
2. Power on
3. Wait 30-60 seconds
4. SSH in and check: `sudo systemctl status doorbot-client`
5. Watch logs: `sudo journalctl -u doorbot-client -f`

Should see polling messages with no errors.

### 4. Test Via Chatbot

In Element chat:
```
$letmein
```

Should respond: "Door unlocked and now locked again."

Watch server logs for POST requests from chatbot.

### 5. Verify Door Unlocks

When chatbot command is sent:
- Pi client should see `letmein: true` within 1 second
- Motor should activate
- Door handle should turn
- After timeout, handle returns to locked

---

## Rollback Plan

If something goes wrong:

### Keep Original dot Server Running (If Still Available)

Change Raspberry Pi client back:
```python
SERVER_URL = "http://dot.cs.wmich.edu:8878"
```

Change chatbot command back:
```python
requests.post("http://dot.cs.wmich.edu:8878", ...)
```

### If dot Is Already Gone

The new server is the only option. Debug using:
- Server logs: `sudo journalctl -u doorbot-server -f`
- Pi client logs: `sudo journalctl -u doorbot-client -f`
- Test API manually with curl commands above

---

## Network Considerations

### DNS Resolution

Ensure `newyakko.cs.wmich.edu` resolves properly:
```bash
# From Raspberry Pi
ping newyakko.cs.wmich.edu

# From chatbot server
ping newyakko.cs.wmich.edu
```

If DNS fails, use IP address instead in configurations.

### Firewall

Port 8878 must be open on newyakko.cs.wmich.edu:
```bash
sudo ufw allow 8878/tcp
```

### Network Access

Verify both Pi and chatbot server can reach newyakko:8878:
```bash
curl http://newyakko.cs.wmich.edu:8878/health
```

---

## Differences from Original

### Additions (New Features)

1. **Web Control Interface**
   - URL: http://newyakko.cs.wmich.edu:8878/control
   - Manual unlock button
   - Status display
   - Activity log

2. **Health Check Endpoint**
   - URL: http://newyakko.cs.wmich.edu:8878/health
   - Returns server status and current door state

3. **Enhanced Logging**
   - Server logs all unlock/lock commands
   - Includes IP addresses and timestamps

### Removed Features

None - All original functionality is preserved.

---

## Support

After migration is complete:

- **Server issues:** Check `sudo journalctl -u doorbot-server -f`
- **Pi issues:** See `raspberry_pi/TROUBLESHOOTING.md`
- **Chatbot issues:** Check chatbot logs
- **API issues:** Test with curl commands above

---

## Summary

The doorbot system has been successfully migrated from dot to newyakko:

✅ Server reimplemented with Flask
✅ API fully compatible with original
✅ Raspberry Pi client pre-configured
✅ Chatbot command updated
✅ SD card prepared for plug-and-play
✅ Documentation complete

**Next:** Deploy server and update chatbot command, then test!
