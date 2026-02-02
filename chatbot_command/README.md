# Element Chatbot Integration

This directory contains the updated `$letmein` command for your Element chatbot.

## Installation

Replace the existing command file on your chatbot server:

**Location:** `sysadmin@newyakko:~/ccawmunity/chatbot/commandcenter/commands/letmein.py`

```bash
# On newyakko.cs.wmich.edu
cd ~/ccawmunity/chatbot/commandcenter/commands/
cp letmein.py letmein.py.backup  # Backup the original
# Then upload the new letmein.py from this directory
```

## What Changed

**Old server:** `http://dot.cs.wmich.edu:8878`
**New server:** `http://newyakko.cs.wmich.edu:8878`

The API is identical, so only the URL needed to change.

## Testing

After updating the file and restarting your chatbot:

1. In your Element chat, send: `$letmein`
2. The chatbot should respond: "Door unlocked and now locked again."
3. Check server logs to see the unlock command was received

## How It Works

```
User sends: $letmein in Element chat
     ↓
Chatbot executes letmein.py
     ↓
POST {"status": {"letmein": True}} to newyakko.cs.wmich.edu:8878
     ↓
Server sets letmein = True
     ↓
Raspberry Pi polls server (every 1 second)
     ↓
Pi receives letmein = True
     ↓
Pi unlocks door
     ↓
After 3 seconds, chatbot sends: POST {"status": {"letmein": False}}
     ↓
Server sets letmein = False
     ↓
Door re-locks
```

## Full Server URL

If your chatbot server can't resolve `newyakko.cs.wmich.edu`, you may need to use the IP address instead. Update line 27 in `letmein.py`:

```python
response = requests.post("http://IP_ADDRESS:8878", ...)
```
