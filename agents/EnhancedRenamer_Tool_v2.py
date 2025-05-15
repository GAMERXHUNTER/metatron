# EnhancedRenamer_Tool_v2.py
# Improved file renamer for _enhanced.md files

import os
import re

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
REPORT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault/VaultAgentLogs", "renamed_files_v2.md"))
os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)

def extract_title_candidate(content):
    # Try extracting from Key Ideas section
    match = re.search(r"##\s*Key Ideas\s*(.*?)\n##", content, re.DOTALL | re.IGNORECASE)
    if not match:
        match = re.search(r"##\s*Key Ideas\s*(.*)", content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip().split("\n")[0]
    
    # Fallback: use first H2 heading in document
    match = re.search(r"##\s+(.*?)\n", content)
    if match:
        return match.group(1).strip()
    
    return None

def sanitize(text):
    clean = re.sub(r'[^a-zA-Z0-9 ]', '', text).strip().replace(" ", "_")
    return clean[:60]

def rename_files():
    renamed = []
    skipped = []

    for root, _, files in os.walk(VAULT_DIR):
        for fname in files:
            if fname.endswith("_enhanced.md"):
                path = os.path.join(root, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()

                    candidate = extract_title_candidate(content)
                    if not candidate:
                        skipped.append((fname, "No title found"))
                        continue

                    short_title = sanitize(candidate)
                    if short_title in fname:
                        skipped.append((fname, "Already renamed"))
                        continue

                    # Extract video/content ID from filename
                    id_match = re.search(r"([a-zA-Z0-9_-]+)_enhanced\.md", fname)
                    if not id_match:
                        skipped.append((fname, "Could not extract ID"))
                        continue

                    original_id = id_match.group(1)
                    new_name = f"{short_title}_{original_id}_enhanced.md"
                    new_path = os.path.join(root, new_name)

                    if path != new_path:
                        os.rename(path, new_path)
                        renamed.append((fname, new_name))
                        print(f"[RENAMED] {fname} → {new_name}")

                except Exception as e:
                    skipped.append((fname, f"Error: {e}"))

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# EnhancedRenamer v2 Report\n\n")
        f.write(f"## Renamed Files ({len(renamed)})\n")
        for old, new in renamed:
            f.write(f"- {old} → {new}\n")
        f.write(f"\n## Skipped Files ({len(skipped)})\n")
        for fname, reason in skipped:
            f.write(f"- {fname}: {reason}\n")

    print(f"✅ Rename complete. Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    rename_files()
