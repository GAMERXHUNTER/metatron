
# 🧠 Metatron Project — Quickstart Guide

Welcome to the Metatron AI system. This quickstart guide explains how to initialize and run your automated intelligence environment using this project bundle.

---

## 🧱 1. Folder Structure

After unzipping, your project should look like:

```
/metatron_project/
│
├── activate_metatron.py
├── scheduler_mastermold_runner.py
├── metatron_project_manifest.json
├── README.md
│
├── /agents/          → Python tools
├── /launchers/       → Windows .bat launchers
├── /docs/            → Instruction and strategy files
├── /Vault/           → Vault content input/output
├── /Logs/            → System logs
├── /Outputs/         → Enhanced content exports
```

---

## 🚀 2. Start Here: Activate Metatron

Run the bootstrap script:

```bash
python activate_metatron.py
```

This will:
- Check folder integrity
- Show available agents and tools
- Let you launch agents like:
  - VaultProcessor_AI
  - VaultEnhancer_AI
  - VaultGPT_Plus_Agent
  - Mastermold Orchestrator

---

## ⏳ 3. Optional: Schedule Mastermold

To automatically run `Mastermold_Orchestrator.py` every 60 minutes:

```bash
python scheduler_mastermold_runner.py
```

✅ Great for passive job execution or daily vault upkeep.

---

## 🧪 4. Test Example Workflow

Example usage pattern:

1. Place raw `.txt` or `.md` files into `/Vault/Raw`
2. Run:
   - `VaultProcessor_AI.py` → Converts raw to clean
   - `VaultEnhancer_AI.py` → Extracts structure
   - `EnhancedRenamer_Tool.py` → Renames for clarity
3. Use `VaultGPT_Plus_Agent.py` to ask questions of your vault

---

## 💡 5. Explore Docs

- `docs/Metatron_MasterGPT_Instructions_Structured.md` → Full capabilities
- `docs/Metatron_MasterGPT_Instructions_Compressed.md` → Token-efficient
- `docs/TimeMasteryApp_ProjectSummary_andFeatureLog.md` → Related subsystem

---

👑 Glory to God. Run the system. Deploy your empire.
