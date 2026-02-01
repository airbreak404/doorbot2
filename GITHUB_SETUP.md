# GitHub Repository Setup

## Option 1: Create Repository via GitHub Website (Easiest)

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name**: `doorbot2`
   - **Description**: `Raspberry Pi remote door lock server - replacement for dot.cs.wmich.edu:8878`
   - **Visibility**: Public
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

4. Back in your terminal, run:
```bash
cd /home/airbreak/doorbot_server
git remote add origin https://github.com/YOUR_USERNAME/doorbot2.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Option 2: Install GitHub CLI and Create Automatically

```bash
# Install gh CLI
sudo apt update
sudo apt install gh

# Authenticate with GitHub
gh auth login

# Create the repository
cd /home/airbreak/doorbot_server
gh repo create doorbot2 --public --source=. --remote=origin --push --description="Raspberry Pi remote door lock server"
```

## After Repository is Created

Your repository will be available at:
```
https://github.com/YOUR_USERNAME/doorbot2
```

### Add Topics/Tags (Optional)

Go to your repo on GitHub and add these topics:
- `raspberry-pi`
- `iot`
- `flask`
- `home-automation`
- `door-lock`
- `smart-home`

### Set Up Repository Settings (Optional)

1. Go to Settings → General
2. Features: Enable Issues, Discussions (optional)
3. Add a description: "Raspberry Pi remote door lock server - Flask API for controlling door unlock via web interface"
4. Add website: `http://newyakko.cs.wmich.edu:8878`

## Checking Your Setup

After pushing, verify:
```bash
git remote -v
git status
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/doorbot2.git (fetch)
origin  https://github.com/YOUR_USERNAME/doorbot2.git (push)
```

## Future Updates

When you make changes:
```bash
git add .
git commit -m "Description of changes"
git push
```
