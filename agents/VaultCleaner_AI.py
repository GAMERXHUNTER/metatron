# VaultCleaner_AI.py (v2.0)
# Removes malformed _enhanced.md files, orphans, and duplicates. Uses vault_recheck_report.md for guidance.

import os
import shutil
import hashlib
import re

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
TRASH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault_Trash"))
REPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault/VaultAgentLogs", "vault_recheck_report.md"))
os.makedirs(TRASH_DIR, exist_ok=True)

def hash_file(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_bad_files_from_report():
    if not os.path.exists(REPORT_PATH):
        print("[WARNING] No recheck report found.")
        return set()
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return {line.split(" ")[1] for line in lines if line.startswith("- ⚠️")}

def move_to_trash(path):
    target = os.path.join(TRASH_DIR, os.path.basename(path))
    shutil.move(path, target)
    print(f"[TRASHED] {os.path.basename(path)}")

def clean_duplicates_and_bad_files():
    seen_hashes = {}
    bad_files = load_bad_files_from_report()
    orphaned_raw = set()
    removed_count = 0

    for root, _, files in os.walk(VAULT_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)

            # Remove malformed _enhanced.md files
            if fname in bad_files:
                move_to_trash(fpath)
                removed_count += 1
                continue

            # Remove duplicates
            try:
                file_hash = hash_file(fpath)
                if file_hash in seen_hashes:
                    print(f"[DUPLICATE] {fname} matches {seen_hashes[file_hash]}")
                    move_to_trash(fpath)
                    removed_count += 1
                else:
                    seen_hashes[file_hash] = fname
            except Exception as e:
                print(f"[ERROR] Hashing failed for {fname}: {e}")

            # Detect orphaned raw files with no matching _enhanced
            if fname.endswith(".md") and not fname.endswith("_enhanced.md"):
                base = os.path.splitext(fname)[0]
                enhanced_version = os.path.join(root, f"{base}_enhanced.md")
                if not os.path.exists(enhanced_version):
                    orphaned_raw.add(fpath)

    # Trash orphaned raw files
    for f in orphaned_raw:
        print(f"[ORPHANED] No enhanced version found for {os.path.basename(f)}")
        move_to_trash(f)
        removed_count += 1

    print(f"✅ Vault cleaning complete. {removed_count} files moved to trash.")

if __name__ == "__main__":
    clean_duplicates_and_bad_files()
