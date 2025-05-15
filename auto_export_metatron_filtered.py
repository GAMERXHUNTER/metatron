
import os
import shutil
import json
from datetime import datetime

EXPORT_DIR = "exports"
SOURCE_DIR = "."
VERSION_FILE = "VERSION"
MANIFEST_FILE = "metatron_project_manifest.json"
EXCLUDE_DIRS = {"Vault", "Logs", "Outputs", "exports", "__pycache__"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
EXCLUDE_EXT = {".db", ".sqlite", ".pyc"}

def load_current_version():
    try:
        with open(VERSION_FILE, 'r') as f:
            ver = f.read().strip()
            return ver.split()[-1]
    except:
        return "v1.0"

def bump_version(version):
    try:
        major, minor = version.replace('v','').split('.')
        return f"v{major}.{int(minor)+1}"
    except:
        return "v1.1"

def write_new_version(new_version):
    with open(VERSION_FILE, 'w') as f:
        f.write(f"Metatron {new_version} – {datetime.today().strftime('%Y-%m-%d')}")

def append_changelog(version):
    path = os.path.join(EXPORT_DIR, "CHANGELOG.md")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"## {version} – {timestamp}\n- Manual entry: ADD YOUR NOTES HERE\n\n"
    with open(path, 'a') as f:
        f.write(entry)

def zip_filtered(output_path):
    with shutil.make_archive(output_path, 'zip', root_dir=SOURCE_DIR) as archive:
        pass

def filtered_copytree(src_dir, temp_dir):
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        if rel_path == ".":
            rel_path = ""
        if any(part in EXCLUDE_DIRS for part in rel_path.split(os.sep)):
            continue
        for file in files:
            if file in EXCLUDE_FILES or os.path.splitext(file)[1] in EXCLUDE_EXT:
                continue
            src_file = os.path.join(root, file)
            dest_file = os.path.join(temp_dir, rel_path, file)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)

def main():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    current_version = load_current_version()
    new_version = bump_version(current_version)
    print(f"📦 Exporting new version: {new_version}")

    # Prepare temp export folder
    temp_dir = os.path.join(EXPORT_DIR, f"_export_tmp_{new_version}")
    os.makedirs(temp_dir, exist_ok=True)

    # Copy only allowed content
    filtered_copytree(SOURCE_DIR, temp_dir)

    # Create final zip
    archive_name = f"metatron_github_bundle_{new_version}"
    shutil.make_archive(os.path.join(EXPORT_DIR, archive_name), 'zip', temp_dir)

    # Clean up temp
    shutil.rmtree(temp_dir)

    # Update version + changelog
    write_new_version(new_version)
    append_changelog(new_version)
    print(f"✅ Bundle saved to: {EXPORT_DIR}/{archive_name}.zip")

if __name__ == "__main__":
    main()
