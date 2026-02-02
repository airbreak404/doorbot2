# 🚀 Doorbot2 Deployment Checklist

**Complete step-by-step checklist for deploying your Doorbot system**

---

## ✅ What's Already Done

- [x] Server code written and tested
- [x] Raspberry Pi client pre-configured
- [x] SD card prepared and ready (ejected)
- [x] API matches original dot.cs.wmich.edu exactly
- [x] Comprehensive documentation created (80+ KB)
- [x] GitHub repository set up and pushed
- [x] All commits synchronized

**GitHub Repository:** https://github.com/airbreak404/doorbot2

---

## 📋 Deployment Steps

### Phase 1: Raspberry Pi Setup ✅ DONE

- [x] SD card prepared with client
- [x] Auto-start service configured
- [x] WiFi configured (SSID: morgana)
- [x] Client points to newyakko.cs.wmich.edu:8878
- [x] Desktop README created
- [x] SD card safely ejected

**Status:** SD card is ready to insert into Raspberry Pi

---

### Phase 2: Server Deployment 🔄 READY TO DO

**On newyakko.cs.wmich.edu:**

1. **Clone repository:**
   ```bash
   cd ~
   git clone https://github.com/airbreak404/doorbot2.git
   cd doorbot2
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Test the server:**
   ```bash
   python3 server.py
   ```
   Should see:
   ```
   🚪 Doorbot Server Starting
   Server: newyakko.cs.wmich.edu
   Port: 8878
   ```

4. **Test API:**
   ```bash
   # In another terminal
   curl http://localhost:8878/health
   # Should return JSON with status: healthy
   ```

5. **Set up systemd service (optional but recommended):**
   ```bash
   sudo cp doorbot-server.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable doorbot-server
   sudo systemctl start doorbot-server
   sudo systemctl status doorbot-server
   ```

6. **Open firewall:**
   ```bash
   sudo ufw allow 8878/tcp
   ```

7. **Verify externally accessible:**
   ```bash
   # From another machine
   curl http://newyakko.cs.wmich.edu:8878/health
   ```

**Checklist:**
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Server starts without errors
- [ ] Health check passes
- [ ] systemd service running
- [ ] Firewall allows port 8878
- [ ] Externally accessible

---

### Phase 3: Element Chatbot Update 🔄 READY TO DO

**On newyakko.cs.wmich.edu:**

1. **Backup current command:**
   ```bash
   cd ~/ccawmunity/chatbot/commandcenter/commands/
   cp letmein.py letmein.py.backup
   ```

2. **Update the command:**
   ```bash
   # Edit letmein.py
   nano letmein.py
   ```

3. **Change line 27 from:**
   ```python
   response = requests.post("http://dot.cs.wmich.edu:8878", ...)
   ```

4. **To:**
   ```python
   response = requests.post("http://newyakko.cs.wmich.edu:8878", ...)
   ```

5. **Also update line 36 (the reset POST)**

6. **Add Content-Type header (important!):**
   ```python
   response = requests.post("http://newyakko.cs.wmich.edu:8878",
                           data=json.dumps(data),
                           headers={'Content-Type': 'application/json'})
   ```

7. **Save and restart chatbot**

8. **Test the command:**
   - In Element chat: `$letmein`
   - Should respond: "Door unlocked and now locked again."

**Checklist:**
- [ ] Original command backed up
- [ ] URL updated to newyakko
- [ ] Content-Type header added
- [ ] Chatbot restarted
- [ ] `$letmein` command tested
- [ ] Command responds correctly

**Alternative:** Use the pre-updated file from `chatbot_command/letmein.py`

---

### Phase 4: Raspberry Pi Boot 🔄 READY TO DO

1. **Insert SD card into Raspberry Pi**

2. **Connect to network** (WiFi: morgana - already configured)

3. **Power on the Pi**

4. **Wait 30-60 seconds for boot**

5. **Find Pi's IP address:**
   - Check your router's DHCP leases
   - Or use: `arp -a | grep -i "b8:27:eb"`
   - Or use: `nmap -sn 192.168.1.0/24` (adjust subnet)

6. **SSH into the Pi:**
   ```bash
   ssh Janus@RASPBERRY_PI_IP
   ```

7. **Check client status:**
   ```bash
   sudo systemctl status doorbot-client
   ```
   Should show: `Active: active (running)`

8. **Watch logs:**
   ```bash
   sudo journalctl -u doorbot-client -f
   ```
   Should see:
   ```
   🚪 DOORBOT CLIENT
   Server: http://newyakko.cs.wmich.edu:8878
   Initializing GPIO pins...
   Starting server polling...
   ```

9. **Look for errors:**
   - No "Cannot connect to server" messages
   - No GPIO errors
   - Polling should be successful

**Checklist:**
- [ ] SD card inserted
- [ ] Pi powered on
- [ ] Pi connected to network
- [ ] IP address found
- [ ] SSH connection successful
- [ ] Client service running
- [ ] No errors in logs
- [ ] Server polling working

---

### Phase 5: End-to-End Testing 🔄 READY TO DO

1. **Verify all components running:**
   - [ ] Server: `curl http://newyakko.cs.wmich.edu:8878/health`
   - [ ] Pi client: `sudo systemctl status doorbot-client`
   - [ ] Chatbot: Running and responsive

2. **Test via chatbot:**
   - In Element chat: `$letmein`
   - Watch Pi logs: `sudo journalctl -u doorbot-client -f`
   - Should see unlock sequence within 1 second
   - Door should physically unlock

3. **Test via web interface (optional):**
   - Open: http://newyakko.cs.wmich.edu:8878/control
   - Click "Unlock Door (Manual)"
   - Watch Pi logs
   - Door should unlock

4. **Verify auto-reset:**
   - After chatbot command, wait 3 seconds
   - Check server: `curl http://newyakko.cs.wmich.edu:8878/`
   - Should show: `"letmein": false`

5. **Test reboot persistence:**
   - Reboot Pi: `sudo reboot`
   - Wait for boot
   - Check client auto-starts: `sudo systemctl status doorbot-client`

**Checklist:**
- [ ] Server responding
- [ ] Pi client polling
- [ ] Chatbot sends commands
- [ ] Pi receives unlock signal
- [ ] Motor activates
- [ ] Door physically unlocks
- [ ] Auto-reset works
- [ ] Client survives reboot

---

## 🎉 Success Criteria

Your system is fully operational when:

✅ **Server:**
- Accessible at http://newyakko.cs.wmich.edu:8878
- Health check returns "healthy"
- API responds to GET and POST

✅ **Raspberry Pi:**
- Client auto-starts on boot
- Polls server every 1 second
- No errors in logs
- GPIO control working

✅ **Chatbot:**
- `$letmein` command sends unlock
- Responds with success message
- Auto-resets after 3 seconds

✅ **Integration:**
- Chatbot → Server → Pi → Door (complete chain works)
- Unlock happens within 1 second of command
- Door physically unlocks
- System recovers from reboots

---

## 📊 Monitoring

### Server Logs
```bash
# If using systemd
sudo journalctl -u doorbot-server -f

# If running manually
# Logs print to console
```

### Pi Client Logs
```bash
sudo journalctl -u doorbot-client -f
```

### What to Watch For

**Normal operation:**
```
[timestamp] GET request from RASPBERRY_PI_IP
[timestamp] POST request from CHATBOT_IP
[timestamp] UNLOCK command from CHATBOT_IP
[timestamp] LOCK command from CHATBOT_IP
```

**Problems to investigate:**
```
Connection refused
Timeout errors
GPIO permission denied
Cannot connect to server
```

---

## 🆘 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| Server won't start | Check if port 8878 is in use: `sudo lsof -i :8878` |
| Pi can't reach server | `ping newyakko.cs.wmich.edu` from Pi |
| Chatbot command fails | Check chatbot logs for errors |
| Motor doesn't run | Check GPIO permissions, wiring |
| Client won't start | Check logs: `sudo journalctl -u doorbot-client -n 50` |

**Full troubleshooting:** [raspberry_pi/TROUBLESHOOTING.md](raspberry_pi/TROUBLESHOOTING.md)

---

## 📚 Documentation Reference

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview and quick start |
| [MIGRATION_FROM_DOT.md](MIGRATION_FROM_DOT.md) | Complete migration guide |
| [raspberry_pi/QUICK_START.md](raspberry_pi/QUICK_START.md) | 3-step Pi setup |
| [raspberry_pi/TROUBLESHOOTING.md](raspberry_pi/TROUBLESHOOTING.md) | Problem solutions |
| [chatbot_command/README.md](chatbot_command/README.md) | Chatbot integration |

---

## 🔄 Next Actions

**Right now:**
1. Deploy server on newyakko.cs.wmich.edu
2. Update Element chatbot command
3. Boot Raspberry Pi with prepared SD card
4. Test the complete system

**After successful deployment:**
1. Monitor logs for issues
2. Document any customizations
3. Consider security enhancements (see README.md)
4. Share success with the team! 🎊

---

**Repository:** https://github.com/airbreak404/doorbot2

**Everything is ready. Time to deploy!** 🚀
