
# 🔧 Metatron System Scripts – Control & Automation

This document explains the three core scripts used to control, monitor, and evolve your Metatron AI system.

---

## 🚀 1. `activate_metatron.py` – Bootstrap Launcher

This is your master control menu.

### ✅ What It Does:
- Checks for essential folders and creates them if missing
- Loads and validates `metatron_project_manifest.json`
- Displays a numbered menu to launch:
  - VaultProcessor
  - Enhancer
  - VaultGPT
  - Mastermold
  - Renamer
  - Open README

### 🧪 Usage:
```bash
python activate_metatron.py
```

> Ideal for daily use to run tools from one central place

---

## ⏱ 2. `scheduler_mastermold_runner.py` – Task Loop Automation

Runs `Mastermold_Orchestrator.py` repeatedly on a schedule.

### ✅ What It Does:
- Waits X minutes (default: 60)
- Calls the orchestrator
- Repeats forever (until killed)

### 🧪 Usage:
```bash
python scheduler_mastermold_runner.py
```

### ⚙️ Configuration:
Edit the script line:
```python
INTERVAL_MINUTES = 60
```

> Use this when you want jobs to auto-run every hour without manual input.

---

## 📦 3. `auto_export_metatron.py` – Version Snapshot & Bundler

Creates versioned `.zip` bundles of your full project (excluding Vault).

### ✅ What It Does:
- Increments `VERSION` file (e.g. v1.2 → v1.3)
- Archives current clean project into:
  ```
  /exports/metatron_github_bundle_v1.3.zip
  ```
- Appends a log entry to `CHANGELOG.md`

### 🧪 Usage:
```bash
python auto_export_metatron.py
```

> Use this to backup your system before major changes or pushes to GitHub.

---

These scripts give you command-line control over launching, running, and preserving your AI infrastructure. They're the backbone of the Metatron runtime system.
