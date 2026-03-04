# 📤 Push to GitHub - Step by Step

## Option 1: Create Personal Access Token (PAT)

### Step 1: Create Token
1. Go to: https://github.com/settings/tokens/new
2. Fill in:
   - **Note:** `NLP Analyzer Deployment`
   - **Expiration:** 90 days
   - **Select scopes:** Check the box for `repo` (Full control of private repositories)
3. Scroll down and click **"Generate token"**
4. **COPY the token immediately!** (looks like: `ghp_xxxxxxxxxxxxxxxxxxxx`)

### Step 2: Push with Token
Run this command in your terminal:
```bash
git remote set-url origin https://github.com/codewithvini/indian-language-nlp-analyzer.git
git push -u origin main
```

When prompted:
- **Username:** `codewithvini`
- **Password:** Paste your token (the one starting with `ghp_`)

---

## Option 2: Using VS Code (Easiest!)

1. Open VS Code in your project folder
2. Press `Ctrl + Shift + G` (Source Control)
3. You should see "14 files staged"
4. Click the checkmark ✓ to commit (if not already committed)
5. Click **"Sync Changes"** or **"Push"** button
6. VS Code will prompt you to sign in to GitHub
7. Follow the browser authentication
8. Done! ✅

---

## Option 3: Using GitHub CLI (if installed)

```bash
gh auth login
git push -u origin main
```

---

## ✅ Verify Push Successful

Go to: https://github.com/codewithvini/indian-language-nlp-analyzer

You should see all your files there!

---

## 🚀 After Push is Successful

Next step: Deploy on Render.com!
See DEPLOYMENT_GUIDE.md for full instructions.
