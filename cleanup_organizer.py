
import os
import shutil

# Define target folders
FOLDERS = {
    ".py": "agents",
    ".bat": "launchers",
    ".md": "docs",
    ".json": ".",
    ".txt": "docs",
}

# Define exclusions
EXCLUDED = {
    "activate_metatron.py",
    "scheduler_mastermold_runner.py",
    "auto_export_metatron.py",
    "Run_Metatron.bat",
    "Run_AutoExport.bat",
    "metatron_project_manifest.json",
    "VERSION",
    "README.md",
    "Quickstart.md",
    "cleanup_organizer.py"
}

def move_file(file, ext):
    target = FOLDERS.get(ext, None)
    if target and os.path.exists(file) and file not in EXCLUDED:
        new_path = os.path.join(target, os.path.basename(file))
        print(f"📁 Moving {file} → {new_path}")
        shutil.move(file, new_path)

def main():
    for file in os.listdir("."):
        if os.path.isfile(file):
            _, ext = os.path.splitext(file)
            move_file(file, ext)

if __name__ == "__main__":
    main()
