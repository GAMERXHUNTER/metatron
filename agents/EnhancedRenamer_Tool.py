# EnhancedRenamer_Tool.py
# Renames _enhanced.md files using content from Key Ideas + preserves original ID

import os
import re

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
REPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault/VaultAgentLogs", "renamed_files.md"))
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

def extract_key_idea(content):
    match = re.search(r"##\s*Key Ideas\s*(.*?)\n##", content, re.DOTALL | re.IGNORECASE)
    if not match:
        match = re.search(r"##\s*Key Ideas\s*(.*)", content, re.DOTALL | re.IGNORECASE)
    if match:
        idea = match.group(1).strip().split("\n")[0]
        clean = re.sub(r'[^a-zA-Z0-9 ]', '', idea).strip().replace(" ", "_")
        return clean[:60] if clean else None
    return None

def rename_files():
    renamed = []

    for root, _, files in os.walk(VAULT_DIR):
        for fname in files:
            if fname.endswith("_enhanced.md"):
                path = os.path.join(root, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()

                    key_idea = extract_key_idea(content)
                    if not key_idea:
                        continue

                    # Extract original ID from filename (everything before "_enhanced.md")
                    id_match = re.search(r"([a-zA-Z0-9_-]+)_enhanced\.md", fname)
                    if not id_match:
                        continue

                    original_id = id_match.group(1)
                    new_name = f"{key_idea}_{original_id}_enhanced.md"
                    new_path = os.path.join(root, new_name)

                    if path != new_path:
                        os.rename(path, new_path)
                        renamed.append((fname, new_name))
                        print(f"[RENAMED] {fname} → {new_name}")

                except Exception as e:
                    print(f"[ERROR] Failed to process {fname}: {e}")

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Renamed Enhanced Files Report\n\n")
        for old, new in renamed:
            f.write(f"- {old} → {new}\n")

    print(f"✅ Rename complete. Report saved to: {REPORT_PATH}")

if __name__ == "__main__":
    rename_files()
