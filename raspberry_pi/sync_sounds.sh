#!/bin/bash
# Syncs .wav files from Proton Drive folder to local sounds directory.
# Requires rclone configured with a remote named "protondrive".
# One-time setup: see README.md → Proton Drive Sync section.

SOUNDS_DIR="/home/doorbot/doorbot/sounds"
REMOTE_PATH="protondrive:sounds"

rclone sync "$REMOTE_PATH" "$SOUNDS_DIR" \
    --include "*.wav" \
    --exclude "*" \
    --log-level WARNING
