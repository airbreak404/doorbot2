# 🔒 Safe Deployment & Server Update Guide

**How to safely propose and implement changes to production servers without breaking things**

---

## ⚠️ The Problem This Solves

When working on a production server (like `newyakko.cs.wmich.edu`), you might:
- Accidentally commit server-specific configurations
- Push changes that break production
- Forget to test before deploying
- Make changes directly on the server without version control
- Commit sensitive information (passwords, API keys)

**This guide prevents all of that.** 🛡️

---

## 🎯 Golden Rules

### ✅ **DO**:
1. **Always work in a feature branch**
2. **Test locally before pushing**
3. **Never commit secrets or server-specific configs**
4. **Use Pull Requests for review**
5. **Document what you changed and why**

### ❌ **NEVER**:
1. ~~Commit directly to `main` branch~~
2. ~~Make changes directly on production server without git~~
3. ~~Push untested code~~
4. ~~Commit passwords, API keys, or secrets~~
5. ~~Skip pull request review~~

---

## 🔄 Safe Update Workflow

### Step 1: Start With a Feature Branch

**Never work directly on `main`.** Always create a branch:

```bash
# Clone the repo (first time only)
git clone https://github.com/airbreak404/doorbot2.git
cd doorbot2

# Or pull latest changes
git checkout main
git pull origin main

# Create a feature branch
git checkout -b feature/your-change-description
```

**Examples of good branch names:**
- `fix/door-unlock-timeout`
- `feature/add-authentication`
- `update/chatbot-url`
- `docs/deployment-guide`

---

### Step 2: Make Your Changes

Edit files as needed, but **be careful with**:

#### 🚫 **Files You Should NEVER Commit:**
- `.env` files with passwords
- `config.py` with API keys
- Server IP addresses (if they should be configurable)
- SSH keys or credentials
- Private certificates

#### ✅ **What TO Commit:**
- Code changes
- Documentation updates
- Configuration **templates** (not actual configs)
- Scripts and utilities

**Tip:** Check your `.gitignore` file to ensure sensitive files are excluded:

```bash
# View what's ignored
cat .gitignore

# Add a file to .gitignore if needed
echo "secrets.env" >> .gitignore
```

---

### Step 3: Test Locally

**Before pushing, test your changes!**

```bash
# Test the server
python3 server.py

# In another terminal, test the API
curl http://localhost:8878/health
curl http://localhost:8878/

# If testing client (requires Raspberry Pi or mock)
python3 raspberry_pi/doorbot_client.py
```

**Run any existing tests:**
```bash
# If test scripts exist
./test_server.sh
```

---

### Step 4: Commit Your Changes

Write clear commit messages explaining **what** and **why**:

```bash
# Stage your changes
git add server.py
git add README.md

# Commit with descriptive message
git commit -m "Fix unlock timeout issue

- Increased timeout from 3s to 5s
- Added error handling for connection failures
- Updated documentation with new timeout value"
```

**Good commit message format:**
```
Brief summary (50 chars or less)

- Bullet point of what changed
- Another change
- Why this change was needed
```

---

### Step 5: Push Your Branch

**Push to GitHub, NOT to production:**

```bash
git push origin feature/your-change-description
```

**This is safe because:**
- Changes go to GitHub, not to the live server
- Other people can review
- You can test more before deploying
- Easy to revert if something's wrong

---

### Step 6: Create a Pull Request

1. **Go to GitHub:** https://github.com/airbreak404/doorbot2
2. **Click "Pull requests" → "New pull request"**
3. **Select your branch**
4. **Fill out the PR description:**

```markdown
## What does this change?
Fixes the door unlock timeout issue that was causing failures.

## Why is this needed?
The 3-second timeout was too short for slow network conditions.

## Testing done:
- [x] Tested locally with server.py
- [x] Verified unlock command works
- [x] Checked no breaking changes to API

## Deployment notes:
Requires server restart after deployment.
```

5. **Request review** (if working with a team)
6. **Wait for approval**

---

### Step 7: Deploy to Production Server

**Only after PR is approved and merged to `main`:**

#### Option A: Pull Latest Changes on Server

```bash
# SSH to production server
ssh airbreak@newyakko.cs.wmich.edu

# Navigate to doorbot directory
cd ~/doorbot2

# Check current status
git status
git log --oneline -5

# Pull latest changes from main
git pull origin main

# Restart the service
sudo systemctl restart doorbot-server

# Check it's running
sudo systemctl status doorbot-server
sudo journalctl -u doorbot-server -n 20
```

#### Option B: Fresh Deployment

```bash
# SSH to production server
ssh airbreak@newyakko.cs.wmich.edu

# Backup current version
mv doorbot2 doorbot2_backup_$(date +%Y%m%d)

# Clone fresh copy
git clone https://github.com/airbreak404/doorbot2.git
cd doorbot2

# Install/update dependencies
pip3 install -r requirements.txt

# Restart service
sudo systemctl restart doorbot-server
```

---

## 🛡️ Protecting Secrets

### Use Environment Variables

**Instead of hardcoding secrets in code:**

```python
# ❌ BAD - Never commit this!
API_KEY = "sk_live_abc123xyz"
DATABASE_PASSWORD = "super_secret_password"
```

**Do this instead:**

```python
# ✅ GOOD - Safe to commit
import os

API_KEY = os.environ.get('API_KEY', 'default_for_dev')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
```

**On the server, set environment variables:**

```bash
# Add to ~/.bashrc or systemd service file
export API_KEY="sk_live_abc123xyz"
export DB_PASSWORD="super_secret_password"
```

### Use Configuration Templates

Create a template that can be committed:

**config.template.py:**
```python
# Configuration template - copy to config.py and fill in values

SERVER_HOST = "YOUR_SERVER_HERE"
SERVER_PORT = 8878
API_KEY = "YOUR_API_KEY_HERE"
```

**In .gitignore:**
```
config.py
.env
secrets/
```

**In README:**
```markdown
## Setup
Copy `config.template.py` to `config.py` and fill in your values.
```

---

## 🔍 Pre-Deployment Checklist

Before deploying to production, verify:

- [ ] Changes tested locally
- [ ] No secrets in commits (`git log -p | grep -i password`)
- [ ] Documentation updated if needed
- [ ] Breaking changes documented
- [ ] PR approved by reviewer
- [ ] Backup of current production version
- [ ] Rollback plan ready
- [ ] Server maintenance window scheduled (if needed)

---

## 🚨 Emergency Rollback

If something goes wrong after deployment:

```bash
# SSH to server
ssh airbreak@newyakko.cs.wmich.edu

# Check git history
cd ~/doorbot2
git log --oneline -10

# Rollback to previous commit
git reset --hard <previous-commit-hash>

# Or rollback one commit
git reset --hard HEAD~1

# Restart service
sudo systemctl restart doorbot-server

# Verify it's working
curl http://localhost:8878/health
```

**Or use the backup:**
```bash
# Stop current service
sudo systemctl stop doorbot-server

# Restore backup
rm -rf doorbot2
mv doorbot2_backup_20260201 doorbot2

# Start service
sudo systemctl start doorbot-server
```

---

## 📝 Example: Safe Change Workflow

Here's a complete example of updating the server URL:

```bash
# 1. Create branch
git checkout main
git pull
git checkout -b update/server-url

# 2. Make changes
nano server.py  # Update configuration

# 3. Test locally
python3 server.py
curl http://localhost:8878/health  # ✅ Working

# 4. Commit
git add server.py
git commit -m "Update server URL configuration

- Changed hardcoded URL to environment variable
- Added fallback to localhost for development
- Updated documentation"

# 5. Push
git push origin update/server-url

# 6. Create PR on GitHub
# (Use web interface)

# 7. After PR merged, deploy
ssh airbreak@newyakko.cs.wmich.edu
cd ~/doorbot2
git pull origin main
sudo systemctl restart doorbot-server
sudo systemctl status doorbot-server  # ✅ Active
```

---

## 🤝 Working With Others

### When Multiple People Deploy

**Use a deployment log:**

Create `DEPLOYMENT_LOG.md`:

```markdown
# Deployment History

## 2026-02-02 - v1.2.0
- Deployed by: airbreak
- Changes: Added authentication system
- Commit: abc123
- Status: ✅ Successful

## 2026-02-01 - v1.1.5
- Deployed by: teammate
- Changes: Fixed timeout issue
- Commit: def456
- Status: ✅ Successful
```

**Coordinate deployments:**
- Announce in chat before deploying
- Check if anyone else is working on the server
- Deploy during low-traffic times
- Have someone available to verify

---

## 🔧 Testing on Server (Non-Production)

If you need to test on the server without affecting production:

```bash
# Clone to a test directory
ssh airbreak@newyakko.cs.wmich.edu
git clone https://github.com/airbreak404/doorbot2.git doorbot2_test
cd doorbot2_test
git checkout feature/your-branch

# Run on different port
python3 server.py --port 8879

# Test
curl http://newyakko.cs.wmich.edu:8879/health

# When done, remove test directory
cd ~
rm -rf doorbot2_test
```

---

## 📚 Related Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - General contribution guidelines
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Full deployment steps
- **[README.md](README.md)** - Project overview and setup

---

## 🆘 I Accidentally Committed Secrets!

**If you committed passwords or secrets:**

### 1. Don't Panic
The sooner you act, the better.

### 2. Remove From History

```bash
# Install BFG Repo-Cleaner
brew install bfg  # or download from https://rtyley.github.io/bfg-repo-cleaner/

# Remove secrets from history
bfg --replace-text secrets.txt .git

# Push the cleaned history
git push --force origin main
```

### 3. Rotate the Secret
**Immediately change the password/key that was exposed!**
- Generate new API key
- Change password
- Revoke compromised credentials
- Update server with new credentials

### 4. Check GitHub Security Alerts
GitHub will email you if it detects exposed secrets.

---

## ✨ Summary

**Safe workflow in 7 steps:**

1. **Branch:** `git checkout -b feature/my-change`
2. **Change:** Edit files (no secrets!)
3. **Test:** Run locally first
4. **Commit:** `git commit -m "Clear message"`
5. **Push:** `git push origin feature/my-change`
6. **PR:** Create pull request on GitHub
7. **Deploy:** Pull changes on server after merge

**Remember:**
- Feature branches prevent accidents
- PRs enable review
- Testing catches bugs before production
- Never commit secrets
- Always have a rollback plan

---

**Questions?** See [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue!

**Repository:** https://github.com/airbreak404/doorbot2
