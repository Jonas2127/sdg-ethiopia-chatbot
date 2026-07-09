# 🚀 Complete Deployment Steps - Follow Along

## ✅ STEP 1: Configuration Files (COMPLETED)
- ✅ Created `.streamlit/config.toml`
- ✅ Created `.streamlit/secrets.toml` (with your API keys)
- ✅ Updated `.gitignore` to protect secrets
- ✅ Git initialized and first commit created

---

## 📍 STEP 2: Create GitHub Repository

### **What you need to do:**

1. **Open your web browser** and go to: https://github.com/new

2. **Fill in the form:**
   - **Repository name**: `sdg-ethiopia-chatbot`
   - **Description**: `AI-powered chatbot for Ethiopia's SDG data - Web + Telegram bot`
   - **Visibility**: Choose **Public** (so Streamlit Cloud can access it)
   - **DON'T check** "Initialize with README" (we already have one)

3. **Click**: "Create repository"

4. **After creation**, you'll see a page with instructions. **Copy the URL** that looks like:
   ```
   https://github.com/YOUR_USERNAME/sdg-ethiopia-chatbot.git
   ```

### **What I'll do next:**
Once you tell me your GitHub username, I'll help you push the code to GitHub.

---

## 📍 STEP 3: Push Code to GitHub

### **I'll run these commands for you:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/sdg-ethiopia-chatbot.git
git branch -M main
git push -u origin main
```

**Note**: You might be asked to login to GitHub. Use your GitHub credentials.

---

## 📍 STEP 4: Deploy on Streamlit Cloud (Web Interface)

### **What you need to do:**

1. **Open**: https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click**: "New app" button (top right)

4. **Fill in the deployment form:**
   - **Repository**: Select `YOUR_USERNAME/sdg-ethiopia-chatbot`
   - **Branch**: `main`
   - **Main file path**: `app.py`

5. **Click**: "Advanced settings" (bottom of form)

6. **In "Secrets" text area**, paste this:**
   ```toml
   GOOGLE_API_KEY = "AIzaSyAb8RN6Ki6oKTlovQ5uV-Nrub1VEBKaWxM-o3LzsE1tf0Wxk3KA"
   TELEGRAM_BOT_TOKEN = "8870174152:AAEob2f_M92jBjhJWHobH7uArdFv4sNne5Y"
   ```

7. **Click**: "Deploy!"

8. **Wait 3-5 minutes** - Streamlit will install everything and start your app

9. **You'll get a URL** like: `https://sdg-ethiopia-chatbot-xxxxx.streamlit.app`

### **⚠️ IMPORTANT NOTES:**
- The deployment will take a few minutes
- You might see some warnings during build - that's normal
- The `chroma_db` folder won't be uploaded (it's in .gitignore), so you'll need to handle vector database differently

---

## 📍 STEP 5: Handle Vector Database Issue

### **Problem**: 
Your local `chroma_db` folder (11,346 documents) is NOT uploaded to GitHub because it's too large.

### **Solution - Option A (Recommended):**
Upload your ChromaDB to cloud storage and download it when the app starts:

I'll create a script that:
1. Checks if `chroma_db` exists
2. If not, downloads it from a cloud link (Google Drive, Dropbox, etc.)
3. Uses cached version for faster subsequent loads

### **Solution - Option B:**
Rebuild the vector database in Streamlit Cloud (slower first load)

**Which solution do you prefer?**

---

## 📍 STEP 6: Deploy Telegram Bot on Render.com

### **What you need to do:**

1. **Open**: https://render.com

2. **Sign up** with your GitHub account

3. **Click**: "New +" → "Background Worker"

4. **Connect your repository:**
   - Select `YOUR_USERNAME/sdg-ethiopia-chatbot`
   - Click "Connect"

5. **Fill in the form:**
   - **Name**: `sdg-ethiopia-telegram-bot`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python telegram_bot.py`

6. **Add Environment Variables** (click "Add Environment Variable"):
   - **Key**: `GOOGLE_API_KEY`
   - **Value**: `AIzaSyAb8RN6Ki6oKTlovQ5uV-Nrub1VEBKaWxM-o3LzsE1tf0Wxk3KA`
   
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `8870174152:AAEob2f_M92jBjhJWHobH7uArdFv4sNne5Y`

7. **Click**: "Create Background Worker"

8. **Wait 2-3 minutes** for deployment

9. **Check logs** to confirm bot is running

---

## 📍 STEP 7: Test Everything

### **Test Web Interface:**
1. Open your Streamlit URL
2. Try asking: "What is Ethiopia's poverty rate?"
3. Check if live data is fetched

### **Test Telegram Bot:**
1. Open Telegram on your phone
2. Search for your bot: `@your_bot_username`
3. Click "Start"
4. Send: `/help`
5. Ask a question

---

## 📍 STEP 8: Share with ESS Advisors

### **I'll create for you:**
1. **Access Guide PDF** with URLs and instructions
2. **QR Codes** for easy mobile access
3. **Email template** to send to advisors

---

## 🎯 Current Status

✅ **COMPLETED:**
- Configuration files created
- Git initialized and committed
- Ready for GitHub upload

⏳ **NEXT STEP:**
**You need to create GitHub repository and tell me your GitHub username**

Then we'll continue together!

---

## 📞 Questions?

If you have questions at any step, just ask me and I'll explain in detail!

**Ready to continue? Create the GitHub repository now! 🚀**
