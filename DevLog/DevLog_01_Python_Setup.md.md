# 📾 Devlog — Entry #1  
**Date:** `2025-10-31`  
**Phase:** Environment Setup (Steps 1–3)  
**Goal:** Prepare a clean Python development environment for the game prototype.

---

## 🧬 Summary

We set up the foundation for the project, ensuring the environment is isolated, version-controlled, and recognized by VS Code.

---

## ✅ Steps Completed

### **Step 1 – Requirements**
- Installed **Python 3.10+** (recommended 3.11)
- Installed **VS Code** and **Git**
- Created a **GitHub account**
- Verified availability of:
  - `python`, `pip`, and `venv`
  - `git` command line tool
- Confirmed environment works via version checks

---

### **Step 2 – Folder & Repository Setup**
- Created main project folder:
  ```bash
  mkdir game-prototype && cd game-prototype
  ```
- Initialized Git repository:
  ```bash
  git init
  ```
- Created and activated virtual environment:
  ```bash
  python -m venv .venv
  source .venv/bin/activate    # or .venv\Scripts\activate on Windows
  ```
- Verified Python and pip within `.venv`

---

### **Step 3 – VS Code Configuration**
- Opened project in VS Code (`code .`)
- Installed extensions:
  - Python (`ms-python.python`)
  - Pylance (`ms-python.vscode-pylance`)
  - GitLens (optional)
- Selected `.venv` interpreter
- Added workspace settings:
  ```json
  {
    "python.defaultInterpreterPath": ".venv",
    "python.analysis.autoImportCompletions": true,
    "editor.formatOnSave": true
  }
  ```

---

## 🧠 Notes
- The environment is now isolated and configured.
- Ready to start creating project files and initial code.
- Everything is version-controlled and editor-aware.

---

## 🔜 Next
**Step 4:** Create initial project files (`.gitignore`, `requirements.txt`, and `main.py`).

