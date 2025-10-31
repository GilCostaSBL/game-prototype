# 📾 Devlog — Entry #2  
**Date:** `2025-10-31`  
**Phase:** Initial Project Files (Step 4)  
**Goal:** Create the essential files for the game project and confirm the base environment runs correctly.

---

## 🧬 Summary
We created the initial set of project files required to start the game prototype.  
This included the `.gitignore`, dependency list, and a simple Pygame window to verify the environment works.

---

## ✅ Steps Completed

### **1. Created `.gitignore`**
Added standard Python, VS Code, and OS exclusions:
```gitignore
# Python
__pycache__/
*.pyc
.venv/
.env
.env.*

# VS Code
.vscode/

# OS
.DS_Store
Thumbs.db
```

---

### **2. Created `requirements.txt`**
Listed the core dependency:
```text
pygame
```

---

### **3. Created `main.py`**
Built a minimal Pygame program to test the environment:
```python
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Prototype")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    pygame.display.flip()

pygame.quit()
sys.exit()
```

---

### **4. Verified Everything Works**
Executed the following commands:
```bash
pip install -r requirements.txt
python main.py
```
Result: a gray 800×600 window appeared with the title **“Game Prototype”** ✅  

---

## 🧠 Notes
- The basic environment and display loop work correctly.  
- Pygame successfully initialized, confirming dependencies install without conflict.  
- The project structure is now ready for modular expansion.

---

## 🔜 Next
**Step 5:** Verify and lock dependencies (`pip freeze`), ensuring reproducible installs for collaborators or future setups.