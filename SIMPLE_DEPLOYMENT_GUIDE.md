# ✨ Simple 30-Minute Deployment Guide

Follow these steps **in order**. I'll help you with each one!

---

## 🎯 Overview - What We're Going to Do

```
Your Computer 
    ↓
GitHub (upload code)
    ↓
Streamlit Cloud (web chatbot - 24/7)
    ↓
Render.com (telegram bot - 24/7)
    ↓
✅ Live and running forever!
```

---

## ✅ STEP 1: Setup (ALREADY DONE! ✓)

We already completed:
- ✅ Configuration files
- ✅ Git initialized
- ✅ Code committed
- ✅ Secrets protected

**You're ready for Step 2!**

---

## 📍 STEP 2: Create GitHub Repository (5 minutes)

### **DO THIS NOW:**

1. **Open your browser** → Go to: **https://github.com/new**

2. **Fill in ONLY these fields:**
   ```
   Repository name: sdg-ethiopia-chatbot
   Description: SDG Ethiopia Chatbot - AI-powered data assistant
   Visibility: ○ Public  ← SELECT THIS!
   ```

3. **IMPORTANT**: Leave everything else UNCHECKED!
   - ❌ DON'T check "Add a README file"
   - ❌ DON'T check "Add .gitignore"
   - ❌ DON'T select any license

4. **Click the big green button**: "Create repository"

5. **You'll see a page with code snippets**. Look for a URL that looks like:
   ```
   https://github.com/YOUR_USERNAME/sdg-ethiopia-chatbot.git
   ```

6. **TELL ME**: What is your GitHub username?

---

## 📍 STEP 3: Upload Code to GitHub (2 minutes)

**Once you tell me your username, I'll run the commands to upload your code.**

Example: If your username is "yonasabiyu", I'll push code to:
```
https://github.com/yonasabiyu/sdg-ethiopia-chatbot
```

---

## 📍 STEP 4: Deploy Web Chatbot on Streamlit Cloud (10 minutes)

### **DO THIS:**

1. **Open new tab** → **https://share.streamlit.io/**

2. **Click**: "Continue with GitHub"

3. **Authorize Streamlit** (if asked)

4. **Click**: "New app" (big button, top-right)

5. **Fill in the form:**
   ```
   Repository: sdg-ethiopia-chatbot (select from dropdown)
   Branch: main
   Main file path: app.py
   ```

6. **Click**: "Advanced settings..." (at the bottom)

7. **In the big "Secrets" box, copy-paste this EXACTLY:**
   ```toml
   GOOGLE_API_KEY = "AIzaSyAb8RN6Ki6oKTlovQ5uV-Nrub1VEBKaWxM-o3LzsE1tf0Wxk3KA"
   TELEGRAM_BOT_TOKEN = "8870174152:AAEob2f_M92jBjhJWHobH7uArdFv4sNne5Y"
   ```

8. **Click**: "Deploy!" (big red button)

9. **WAIT 3-5 minutes**. You'll see logs scrolling.

10. **When done**, you'll get a URL like:
    ```
    https://sdg-ethiopia-chatbot-xxxxx.streamlit.app
    ```
    **COPY THIS URL! This is your live chatbot!**

---

## ⚠️ IMPORTANT: Vector Database Issue

**Your app will show an error about ChromaDB not found.**

This is because your local database (11,346 documents) is too big to upload to GitHub.

### **Quick Fix - Two Options:**

**OPTION A: Use only live data (fastest)**
- Edit one line in app.py to skip ChromaDB
- Bot will work with only live data from World Bank + ESS
- I can do this in 1 minute

**OPTION B: Upload database to cloud**
- Upload your `chroma_db` folder to Google Drive
- App downloads it on first run
- Takes longer to set up (~15 minutes)

**Which option do you want?**

---

## 📍 STEP 5: Deploy Telegram Bot (10 minutes)

### **DO THIS:**

1. **Open new tab** → **https://render.com**

2. **Click**: "Get Started for Free"

3. **Sign up with GitHub**

4. **After login, click**: "New +" (top-right) → "Background Worker"

5. **Click**: "Connect repository" → Find and select: `sdg-ethiopia-chatbot`

6. **Fill in:**
   ```
   Name: telegram-bot
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: python telegram_bot.py
   ```

7. **Scroll down to "Environment Variables"**

8. **Click**: "Add Environment Variable" (add TWO variables):

   **First variable:**
   ```
   Key: GOOGLE_API_KEY
   Value: AIzaSyAb8RN6Ki6oKTlovQ5uV-Nrub1VEBKaWxM-o3LzsE1tf0Wxk3KA
   ```

   **Second variable:**
   ```
   Key: TELEGRAM_BOT_TOKEN
   Value: 8870174152:AAEob2f_M92jBjhJWHobH7uArdFv4sNne5Y
   ```

9. **Click**: "Create Background Worker"

10. **WAIT 2-3 minutes**. Watch the logs.

11. **When you see**: "Bot is running!" → **SUCCESS!** ✅

---

## 📍 STEP 6: Test Your Chatbots (5 minutes)

### **Test Web Chatbot:**
1. Open the Streamlit URL you got earlier
2. Type: "What is Ethiopia's poverty rate?"
3. Click "Search"
4. Should see an answer! ✅

### **Test Telegram Bot:**
1. Open Telegram app on your phone
2. Search: `@YourBotUsername` (the one you created with BotFather)
3. Click "Start"
4. Send: `/help`
5. Ask: "What is poverty in Ethiopia?"
6. Should get answer! ✅

---

## 🎉 YOU'RE DONE!

### **Your Chatbot is Now:**
- ✅ Running 24/7
- ✅ Accessible from anywhere
- ✅ Free forever (using free tiers)
- ✅ Auto-updates when you push to GitHub

### **Your URLs:**
```
Web Chatbot: https://sdg-ethiopia-chatbot-xxxxx.streamlit.app
Telegram Bot: https://t.me/YourBotUsername
```

---

## 📤 Share with ESS Advisors

**Send them this message:**

```
🇪🇹 SDG Ethiopia Chatbot - Now Live!

Web Interface: [Your Streamlit URL]
Telegram Bot: [Your Bot Username]

Try asking:
• What is Ethiopia's poverty rate?
• Show education enrollment trends
• Latest child mortality statistics

Available 24/7 | Real-time data from UN, World Bank, ESS
```

---

## 🆘 Having Issues?

**Common problems:**

1. **"ChromaDB not found"** → Choose Option A or B above
2. **"API Key invalid"** → Check if you copied secrets correctly
3. **"Bot not responding"** → Check Render.com logs
4. **"App crashed"** → Check Streamlit Cloud logs

**Tell me the error message and I'll help fix it!**

---

## 📞 Ready to Start?

**Right now, tell me:**
1. Your GitHub username
2. Did you create the GitHub repository? (Yes/No)

Then we continue together! 🚀
