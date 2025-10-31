# 📾 Devlog — Entry #3  
**Date:** `2025-10-31`  
**Phase:** Dependency Locking (Step 5)  
**Goal:** Verify Pygame installation and lock dependency versions for consistent environments.

---

## 🧬 Summary
We confirmed that the environment and initial code run correctly, then locked all dependency versions using `pip freeze`.  
This ensures anyone who clones the repository can recreate the exact same setup.

---

## ✅ Steps Completed

### **1. Verified Pygame Installation**
Executed the test command:
```bash
python main.py
```
Result: The gray 800×600 Pygame window opened and closed cleanly. ✅

---

### **2. Locked Dependencies**
Generated an exact list of installed packages:
```bash
pip freeze > requirements.txt
```
Example content:
```text
pygame==2.6.0
```

---

### **3. Verified and Committed Changes**
Checked `requirements.txt` to confirm version pinning, then committed the update:
```bash
git add requirements.txt
git commit -m "Lock dependencies with pip freeze"
```

---

### **4. Optional Setup for Development Tools**
Prepared for future development dependencies by planning a separate `requirements-dev.txt` file:
```text
# requirements-dev.txt
black
pytest
```

---

## 🧠 Notes
- Dependency versions are now fixed and reproducible.  
- The environment can be safely cloned or rebuilt on another machine.  
- The project is ready for GitHub integration.

---

## 🔜 Next
**Step 6:** Push the repository to GitHub to back up the project and enable collaboration.