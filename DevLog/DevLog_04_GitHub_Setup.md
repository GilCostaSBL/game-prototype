
# 🧾 Devlog Entry #4 — GitHub Repository Setup & Authentication Fix  

**Date:** 2025-10-31  
**Phase:** Step 6 — Push Repository to GitHub  

---

## 🧩 Summary
We connected our local Python project to a new GitHub repository to enable version control, backups, and collaboration. During this step, we also resolved an authentication issue that occurred when pushing the project to GitHub.

---

## 🧰 Steps Completed

### 1. Created a GitHub Repository
- Repository name: `game-prototype`  
- Configured as private/public (based on preference).  
- No initial files added on GitHub (README, .gitignore, or license left empty).  

### 2. Linked Local Project to GitHub
Commands executed in the terminal:
```bash
git branch -M main
git remote add origin https://github.com/<username>/game-prototype.git
```

---

### 3. Attempted First Push
Initial push failed due to authentication issues:
```
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/<username>/game-prototype.git/'
```

---

### 4. Fixed Authentication Issue

#### Option Used: Personal Access Token (PAT)
1. Generated a **Personal Access Token** from  
   **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**  
   with scope: `repo`
2. Replaced password with the token when prompted by Git:
   - **Username:** GitHub username  
   - **Password:** (the new token)
3. Successfully pushed the code using:
   ```bash
   git push -u origin main
   ```

#### Optional Credential Storage
Configured Git to store credentials locally:
```bash
git config --global credential.helper store
```

---

### 5. Verification
- The repository and all files are visible on GitHub.  
- `.venv` and `.vscode` folders remain excluded (per `.gitignore`).  
- DevLog entries and `main.py` are present and synced.  

---

### ✅ Outcome
GitHub integration completed successfully.  
Future commits can now be pushed and tracked without repeating authentication issues.
