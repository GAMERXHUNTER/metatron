# VaultRecheck_Tool.py
# Identifies improperly enhanced markdown files in the vault

import os
import re

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
REPORT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault/VaultAgentLogs", "vault_recheck_report.md"))
EXPECTED_SECTIONS = [
    "Key Ideas", "Philosophy", "Psychology", "Strategy", "Methodology",
    "Process", "How-To Guide", "Impactful Quotes", "Mental Models", "Pitfalls / Don'ts", "Target Audience"
]

def validate_structure(text):
    return sum(1 for section in EXPECTED_SECTIONS if re.search(rf"#+\s*{re.escape(section)}", text, re.IGNORECASE))

def scan_vault():
    bad_files = []
    good_files = []

    for root, _, files in os.walk(VAULT_DIR):
        for fname in files:
            if fname.endswith("_enhanced.md"):
                path = os.path.join(root, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        section_count = validate_structure(content)
                        if section_count >= 9:
                            good_files.append((fname, section_count))
                        else:
                            bad_files.append((fname, section_count))
                except Exception as e:
                    bad_files.append((fname, f"error: {e}"))

    return good_files, bad_files

def generate_report(good, bad):
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Vault Recheck Report")
        f.write(f"**Valid Files:** {len(good)}")
        for fname, count in good:
            f.write(f"- ✅ {fname} ({count} sections found)")
        f.write(f"**Malformed or Incomplete Files:** {len(bad)}")
        for fname, count in bad:
            f.write(f"- ⚠️ {fname} ({count} sections found)")
    print(f"📝 Recheck report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    good, bad = scan_vault()
    generate_report(good, bad)
