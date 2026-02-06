# Git Commands - Quick Reference

## 📍 Where to Run Commands

**Always run git commands from your project root folder:**
```bash
cd c:\Users\bipin\OneDrive\Desktop\literature-survey-system
```

Or in VS Code, open the **Terminal** (Ctrl + `) - it automatically opens in your project folder.

---

## 🔄 When You Make Changes to Your Code

### Step 1️⃣: Check What Changed
```bash
git status
```
This shows which files you modified.

### Step 2️⃣: Add Your Changes
```bash
git add .
```
This stages ALL changed files. Or add specific files:
```bash
git add backend/main.py
git add frontend/app/page.tsx
```

### Step 3️⃣: Commit Your Changes
```bash
git commit -m "Your message describing what you changed"
```

**Good commit message examples:**
- `git commit -m "Fixed BM25 ranking bug"`
- `git commit -m "Added export to PDF feature"`
- `git commit -m "Updated frontend styling"`
- `git commit -m "Fixed citation formatting issue"`

### Step 4️⃣: Push to GitHub
```bash
git push
```
That's it! Your changes are now on GitHub.

---

## ⚡ Quick 3-Command Workflow

Most of the time, you'll just use these 3 commands:

```bash
# 1. Stage all changes
git add .

# 2. Commit with message
git commit -m "Description of changes"

# 3. Push to GitHub
git push
```

---

## 🔍 Useful Commands

### See what you changed:
```bash
git status              # List changed files
git diff                # See line-by-line changes
git log --oneline       # See commit history
```

### Before making changes:
```bash
git pull                # Get latest code from GitHub
```

### If you mess up:
```bash
git checkout -- filename.py      # Undo changes to a file
git reset HEAD~1                 # Undo last commit (keeps changes)
```

---

## 📁 Example Workflow

**Scenario**: You fixed a bug in `backend/ranking.py`

```bash
# 1. Navigate to project
cd c:\Users\bipin\OneDrive\Desktop\literature-survey-system

# 2. Check what changed
git status
# Shows: modified: backend/ranking.py

# 3. Add the change
git add backend/ranking.py
# Or add everything: git add .

# 4. Commit
git commit -m "Fixed BM25 score calculation bug"

# 5. Push to GitHub
git push
```

Done! ✅

---

## 🎯 Quick Tips

1. **Commit often** - Don't wait to make huge commits
2. **Write clear messages** - Describe WHAT and WHY you changed
3. **Pull before push** - If working from multiple computers: `git pull` first
4. **Check status** - Always run `git status` to see what's changed

---

## 🚨 Common Issues

### "Nothing to commit"
You haven't changed any files, or you forgot to save them!

### "Please commit your changes"
You have uncommitted changes. Run:
```bash
git add .
git commit -m "Your message"
```

### "Rejected - non-fast-forward"
Someone (or you from another computer) pushed changes. Run:
```bash
git pull
git push
```

---

## 📝 VS Code Integration (Easier!)

You can also use VS Code's built-in Git:

1. **Make changes** to your code
2. Click **Source Control** icon (left sidebar, 3rd icon)
3. See all changed files
4. Click **+** next to files to stage them (or **+** next to "Changes" to stage all)
5. Type commit message in the box
6. Click **✓ Commit** button
7. Click **⋯ (three dots)** → **Push**

This does the same as the commands! 🎉

---

## ⚙️ One-Time Setup (Already Done!)

You already did this, so you don't need to repeat:
- ✅ `git init` - Create repository
- ✅ `git remote add origin URL` - Link to GitHub
- ✅ `git branch -M main` - Rename branch

---

## 🎓 Summary

**For future changes, just remember these 3 commands:**

```bash
git add .
git commit -m "What you changed"
git push
```

That's all you need! 🚀
