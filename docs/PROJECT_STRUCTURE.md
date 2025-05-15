
# 🧱 Metatron Project Structure Guide

This document describes the ideal folder layout for your Metatron AI project.

```plaintext
metatron_project/
├── activate_metatron.py
├── scheduler_mastermold_runner.py
├── auto_export_metatron.py
├── Run_Metatron.bat
├── Run_AutoExport.bat
├── Run_Cleanup.bat
├── metatron_project_manifest.json
├── VERSION
├── README.md
├── Quickstart.md
│
├── /agents/
│   ├── VaultProcessor_AI.py
│   ├── VaultEnhancer_AI.py
│   ├── VaultGPT_Plus_Agent.py
│   ├── Mastermold_Orchestrator.py
│   └── EnhancedRenamer_Tool.py
│
├── /launchers/
│   ├── Run_Mastermold.bat
│   ├── Run_VaultGPT_Plus_Agent.bat
│   ├── Run_EnhancedRenamer.bat
│
├── /docs/
│   ├── Metatron_MasterGPT_Instructions_Structured.md
│   ├── Metatron_MasterGPT_Instructions_Compressed.md
│   ├── TabernacleDigital_Instructions_MERGED_UPDATED.md
│   ├── TimeMasteryApp_ProjectSummary_andFeatureLog.md
│   └── PROJECT_STRUCTURE.md  ← This file
│
├── /Vault/
│   ├── Raw/
│   ├── Enhanced/
│   ├── VaultAgentLogs/
│   ├── Answers/
│   └── Index/
│
├── /Logs/
├── /Outputs/
└── /exports/
```

> This structure ensures all scripts, documentation, vault content, and automation logic are correctly organized, portable, and GitHub-ready.
