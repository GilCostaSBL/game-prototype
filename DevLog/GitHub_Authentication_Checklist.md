## 🔐 GitHub Reactivation Checklist

**Date:** 2025-10-31  
**Purpose:** Re-enable GitHub authentication on a new computer using a Personal Access Token (PAT).

---

### 🧩 1. Retrieve or Generate Token
1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**  
   👉 https://github.com/settings/tokens
2. Click **“Generate new token (classic)”** → name it (e.g., `"VSCode - Game Prototype"`)
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (optional, for GitHub Actions)
4. Generate and **copy the token** — it will only be shown once.

---

### 💻 2. Configure in VS Code
Open the terminal in your project root:

```bash
Ctrl + `
```

Then set Git to remember your credentials:

```bash
git config --global credential.helper store
```

---

### 🔑 3. Authenticate with GitHub
Run a push command to trigger login:

```bash
git push origin main
```

When prompted:
```
Username for 'https://github.com': <your_github_username>
Password for 'https://github.com': <paste_your_token_here>
```

Press Enter — Git will store your credentials in:  
`C:\Users\<YourName>\.git-credentials`

---

### 🧠 4. Verify Configuration
Check stored configuration:

```bash
git config --global --list
```

Expected output:
```
credential.helper=store
user.name=GilCostaSBL
user.email=<your_github_email>
```

---

### 🚀 5. Confirm Push
Retry your push:
```bash
git push origin main
```

You should see:
```
Enumerating objects: ...
To https://github.com/GilCostaSBL/game-prototype.git
```

---

### 🧩 6. Optional: Verify Remote URL
Ensure you’re using HTTPS (not SSH):

```bash
git remote -v
```

If needed, fix the URL:

```bash
git remote set-url origin https://github.com/GilCostaSBL/game-prototype.git
```

---

✅ Once done, GitHub authentication will persist on this computer — no need to re-enter credentials for future pushes.
