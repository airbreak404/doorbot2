#!/usr/bin/env python3
"""
Cleans up sound filenames to 2-3 word, hyphenated, lowercase format.

Usage:
    python3 clean_filenames.py sounds/
    python3 clean_filenames.py          # defaults to ./sounds/

Rules (in order):
    1. Strip hash-like suffixes  (_6bXErot, _81KHxBA)
    2. Strip trailing numbers    (_1, _7901-951678082)
    3. Collapse repeated chars   (fahhhhhh → fah)
    4. Normalize separators      (underscores → hyphens, lowercase)
    5. Remove noise words        (sound, effect, sfx, short, role, reveal,
                                   with, extra, was, able, to, build, it,
                                   in, a, the, an, of, and, or, for, is)
    6. Deduplicate consecutive   (nick-nick-nick → nick)
    7. Truncate                  (≤3 words → keep; 4+ words → first 2)
"""

import os
import re
import sys

NOISE = {
    'sound', 'effect', 'sfx', 'short', 'role', 'reveal',
    'with', 'extra', 'was', 'able', 'to', 'build', 'it',
    'in', 'a', 'the', 'an', 'of', 'and', 'or', 'for', 'is',
}


def clean(name: str) -> str:
    base, ext = os.path.splitext(name)
    if ext.lower() != '.wav':
        return name

    # 1. Strip hash-like suffixes (mixed alnum, 4+ chars after separator)
    base = re.sub(r'[_-][A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*[0-9][A-Za-z0-9]*$', '', base)
    base = re.sub(r'[_-][0-9][A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*$', '', base)

    # 2. Strip trailing numbers (_1, _7901-951678082)
    base = re.sub(r'[_-][0-9]+(?:[_-][0-9]+)*$', '', base)

    # 3. Collapse 3+ repeated chars to 1
    base = re.sub(r'(.)\1{2,}', r'\1', base)

    # 4. Normalize separators
    base = base.replace('_', '-').lower().strip('-')

    # 5. Split and remove noise
    words = [w for w in base.split('-') if w]
    cleaned = [w for w in words if w not in NOISE]
    if not cleaned:
        cleaned = words[:2]  # fallback

    # 6. Deduplicate consecutive repeated words
    deduped = [cleaned[0]] if cleaned else []
    for w in cleaned[1:]:
        if w != deduped[-1]:
            deduped.append(w)
    cleaned = deduped

    # 7. Truncate: keep up to 3 if ≤3, otherwise first 2
    if len(cleaned) > 3:
        cleaned = cleaned[:2]

    return '-'.join(cleaned) + ext


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else 'sounds'
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)

    renamed = 0
    for fname in sorted(os.listdir(directory)):
        if not fname.lower().endswith('.wav'):
            continue
        new_name = clean(fname)
        if new_name == fname:
            continue

        old_path = os.path.join(directory, fname)
        new_path = os.path.join(directory, new_name)

        if os.path.exists(new_path):
            # Clean version already exists (e.g. git re-checked out the
            # original name after a previous rename).  Remove the duplicate.
            os.remove(old_path)
            print(f"  PRUNE {fname} ({new_name} already exists)")
            continue

        os.rename(old_path, new_path)
        print(f"  {fname} → {new_name}")
        renamed += 1

    print(f"\n{renamed} file(s) renamed.")


if __name__ == '__main__':
    main()
