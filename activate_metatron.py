
import os
import json
import subprocess

def print_header():
    print("\n🧠 METATRON SYSTEM INITIALIZER\n" + "="*35)

def check_folders():
    needed = ["agents", "docs", "launchers", "Vault", "Logs", "Outputs"]
    for folder in needed:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Created missing folder: {folder}")
        else:
            print(f"✅ Folder present: {folder}")

def read_manifest():
    manifest_path = "metatron_project_manifest.json"
    if not os.path.exists(manifest_path):
        print("❌ Manifest file missing.")
        return None
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def display_menu(options):
    print("\nWhat would you like to launch?")
    for idx, opt in enumerate(options, 1):
        print(f"[{idx}] {opt}")
    print("[0] Exit")
    choice = input("Enter a number: ")
    return int(choice) if choice.isdigit() and 0 <= int(choice) <= len(options) else -1

def launch_script(path):
    if not os.path.exists(path):
        print(f"❌ Script not found: {path}")
        return
    print(f"🚀 Running {path}...\n")
    subprocess.run(["python", path])

def main():
    print_header()
    check_folders()
    
    manifest = read_manifest()
    if not manifest:
        return

    print("\n📦 Project: " + manifest["project"])
    print("📄 Docs:", len(manifest["entry_docs"]))
    print("🤖 Agents:", len(manifest["agents"]))
    print("🗂 Launchers:", len(manifest["launchers"]))

    menu = [
        "Run VaultProcessor_AI.py",
        "Run VaultEnhancer_AI.py",
        "Run VaultGPT_Plus_Agent.py",
        "Run Mastermold_Orchestrator.py",
        "Run EnhancedRenamer_Tool.py",
        "Open README.md"
    ]

    while True:
        choice = display_menu(menu)
        if choice == 0:
            print("👋 Exiting Metatron Bootstrap.")
            break
        elif 1 <= choice <= 5:
            py_file = manifest["agents"][choice - 1]
            launch_script(py_file)
        elif choice == 6:
            with open("README.md", 'r', encoding='utf-8') as f:
                print("\n" + "="*20 + " README.md " + "="*20)
                print(f.read())
                print("="*52)
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
