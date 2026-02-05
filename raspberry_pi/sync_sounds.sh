#!/bin/bash
# Syncs .wav files from Proton Drive, with a local cache size limit.
# If the sounds folder exceeds MAX_CACHE_MB, oldest files are removed first.
# Requires rclone configured with a remote named "protondrive".

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOUNDS_DIR="$SCRIPT_DIR/sounds"
REMOTE_PATH="protondrive:sounds"
MAX_CACHE_MB=20000  # 20 GB

mkdir -p "$SOUNDS_DIR"

# Pull new sounds from Proton Drive (copy never deletes local files)
rclone copy "$REMOTE_PATH" "$SOUNDS_DIR" \
    --filter "+ *.wav" \
    --filter "- *" \
    --log-level WARNING

# Evict oldest .wav files if cache exceeds limit
CURRENT_KB=$(du -sk "$SOUNDS_DIR" | cut -f1)
MAX_KB=$((MAX_CACHE_MB * 1024))

while [ "$CURRENT_KB" -gt "$MAX_KB" ]; do
    OLDEST=$(find "$SOUNDS_DIR" -name '*.wav' -printf '%T@ %p\n' | sort -n | head -1 | cut -d' ' -f2-)
    [ -z "$OLDEST" ] && break
    rm -f "$OLDEST"
    CURRENT_KB=$(du -sk "$SOUNDS_DIR" | cut -f1)
done
