# 🚨 QUICK FIX - Do This NOW

## Your Problem
Streamlit Cloud app shows:
- ❌ **429 RESOURCE_EXHAUSTED** - API quota limit reached
- ❌ **404 NOT_FOUND** - Wrong model names

## The Fix (3 Steps)

### STEP 1: Push My Code Fixes (30 seconds)
```bash
cd "c:\Users\HP\.vscode\Documents\ESSproject 2\sdg-ethiopia-chatbot"
git add .
git commit -m "Fix: Auto-detect working Gemini models"
git push origin main
```

Wait 2-3 minutes for Streamlit Cloud to redeploy automatically.

---

### STEP 2: Fix the Quota Issue

You have **2 options:**

#### Option A: Wait (Free, but slow)
- Your quota resets at **10 AM Ethiopia time tomorrow**
- Check usage: https://aistudio.google.com/app/apikey

#### Option B: New API Key (Fast, recommended)
1. **Sign out** of current Google account
2. **Sign in** with different Google account
3. Go to: https://aistudio.google.com/app/apikey
4. Click "Create API Key"
5. Copy the key (starts with `AIza...`)
6. Update Streamlit Cloud Secrets:
   - Go to your app dashboard
   - Settings → Secrets
   - Change:
   ```toml
   GOOGLE_API_KEY = "AIzaYourNewKeyHere"
   ```
   - Save
7. Reboot app (click menu ⋮ → Reboot)

---

### STEP 3: Test
- Open your Streamlit Cloud app
- Ask a question
- Should work now! ✅

---

## Why This Happened

1. **Too many API requests** - You hit the 1,500 requests/day limit
2. **Wrong model names** - App was trying deprecated models
3. **I fixed #2**, you need to fix #1 (get new API key OR wait)

---

## Questions?
Read the full guide: `FIX_STREAMLIT_CLOUD.md`
