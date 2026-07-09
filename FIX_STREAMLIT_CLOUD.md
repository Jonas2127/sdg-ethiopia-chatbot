# Fix Streamlit Cloud Deployment Issue

## 🚨 PROBLEM IDENTIFIED

Your Streamlit Cloud app is failing with TWO issues:

### Issue 1: API Quota Exhausted (429 ERROR)
```
429 RESOURCE_EXHAUSTED
```
**You've hit your daily API limit of 1,500 requests.**

### Issue 2: Wrong Model Names (404 ERROR)  
```
404 NOT_FOUND - models/gemini-2.5-flash is no longer available
```
**The app is trying to use models that don't exist.**

---

## ✅ SOLUTIONS

### SOLUTION 1: Wait for Quota Reset (Immediate Fix)

Your Gemini API quota resets daily at:
- **10:00 AM Ethiopia Time**
- **Midnight Pacific Time**

**Check your quota usage:**
1. Visit: https://aistudio.google.com/app/apikey
2. Click your API key
3. Click "View API usage"
4. See how many requests you've used today

**What to do:**
- Wait until 10 AM Ethiopia time
- OR proceed to Solution 2

---

### SOLUTION 2: Get a New API Key from Different Google Account

Since quota is tied to your **Google account** (not the API key), you need to:

1. **Sign OUT of current Google account**
   - Go to: https://accounts.google.com/
   - Click your profile → Sign out

2. **Sign IN with a different Google account**
   - Use a different email (personal, university, etc.)

3. **Create a new API key**
   - Visit: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the full key (starts with `AIza...`)

4. **Update Streamlit Cloud Secrets**
   - Go to your Streamlit Cloud dashboard
   - Open your app
   - Click "Settings" (⚙️)
   - Click "Secrets"
   - Update:
   ```toml
   GOOGLE_API_KEY = "AIzaYourNewKeyHere"
   ```
   - Click "Save"

5. **Reboot the app**
   - Click menu (⋮) → "Reboot app"
   - Wait 2-3 minutes

---

### SOLUTION 3: Push Updated Code (I've Already Fixed It)

I've updated your `app.py` to automatically find working models. Now you need to push to GitHub:

```bash
cd "c:\Users\HP\.vscode\Documents\ESSproject 2\sdg-ethiopia-chatbot"
git add app.py scripts\step2_test_gemini.py
git commit -m "Fix: Auto-detect working Gemini models and handle quota errors"
git push origin main
```

After pushing, Streamlit Cloud will auto-redeploy in 2-3 minutes.

---

## 🎯 RECOMMENDED ACTION PLAN

**Do this NOW:**

1. **Push the code fixes I made:**
   ```bash
   git add .
   git commit -m "Fix Gemini model detection for Streamlit Cloud"
   git push origin main
   ```

2. **Wait for Streamlit Cloud to redeploy** (2-3 minutes)

3. **If still getting 429 errors:**
   - Option A: Wait until 10 AM Ethiopia time tomorrow
   - Option B: Get new API key from different Google account (see Solution 2 above)

4. **Test the app again**

---

## 📊 Understanding API Quotas

### Free Tier Limits:
- **15 requests per minute**
- **1,500 requests per day**
- **Resets:** Midnight Pacific Time = 10 AM Ethiopia Time

### How Many Requests Your App Uses:
- **Each question = 1-2 API calls**
- **Model detection (on startup) = Multiple test calls**
- **If you ask 50 questions = ~100 API calls**
- **If 15 people use the app = Can hit 1,500 quickly**

### How to Reduce API Usage:
1. **Cache responses** (already implemented in your `unified_data_fetcher.py`)
2. **Limit model detection** (I've optimized this in my fix)
3. **Use longer cache duration**
4. **Consider upgrading to paid tier** if this is for production

---

## 🔍 Verify It's Working

After pushing and redeploying, you should see:

✅ **Success indicators:**
- No 429 errors
- No 404 errors
- Model auto-detects successfully
- Questions get answered

❌ **If still failing:**
- Check Streamlit Cloud logs (click "Manage app" → View logs)
- Verify API key is correct in Streamlit secrets
- Confirm you're not still hitting quota (check usage at aistudio.google.com)

---

## 🆘 Still Having Issues?

**Check these:**

1. **API Key Format**
   - Should start with `AIza...`
   - Your current key starts with `AQ.` which is unusual
   - Try generating a fresh key at: https://aistudio.google.com/app/apikey

2. **Streamlit Cloud Logs**
   ```
   Go to app → "Manage app" → View logs
   Look for specific error messages
   ```

3. **Test Locally First**
   ```bash
   python scripts\step2_test_gemini.py
   ```
   If this works locally but fails on cloud, it's definitely a quota or API key issue.

---

## 📝 Next Steps

1. ✅ Push my code fixes (already done above)
2. ⏰ Wait for quota reset OR get new API key
3. 🧪 Test the app
4. 📊 Monitor API usage to avoid hitting limits again

**Your app will work once the quota resets or you get a new API key!**
