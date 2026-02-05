#!/bin/bash
# Syncs sounds from GitHub by fetching and checking out only the sounds/
# directory.  Code changes are NOT applied — those require a manual git pull.
# To add a new sound: upload a .wav to raspberry_pi/sounds/ on GitHub.

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOUNDS_DIR="$REPO_DIR/raspberry_pi/sounds"
MAX_CACHE_MB=20000  # 20 GB

cd "$REPO_DIR" || exit 1

# Fetch latest from remote (no merge)
git fetch origin --quiet

# Update only the sounds directory from remote master
git checkout origin/master -- raspberry_pi/sounds/

# Evict oldest .wav files if cache exceeds limit
CURRENT_KB=$(du -sk "$SOUNDS_DIR" | cut -f1)
MAX_KB=$((MAX_CACHE_MB * 1024))

while [ "$CURRENT_KB" -gt "$MAX_KB" ]; do
    OLDEST=$(find "$SOUNDS_DIR" -name '*.wav' -printf '%T@ %p\n' | sort -n | head -1 | cut -d' ' -f2-)
    [ -z "$OLDEST" ] && break
    rm -f "$OLDEST"
    CURRENT_KB=$(du -sk "$SOUNDS_DIR" | cut -f1)
done
