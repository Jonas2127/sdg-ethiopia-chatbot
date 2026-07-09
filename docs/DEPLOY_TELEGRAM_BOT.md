# Deploy Telegram Bot 24/7 - PythonAnywhere

## Free 24/7 Hosting on PythonAnywhere

### Step 1: Create Account
1. Go to: https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute"
3. Sign up for **FREE Beginner account**

### Step 2: Upload Your Project
1. In PythonAnywhere dashboard, go to **Files**
2. Create folder: `sdg-ethiopia-chatbot`
3. Upload these files:
   - `telegram_bot.py`
   - `.env` (with your API keys)
   - `requirements.txt`
   - `chroma_db/` folder (entire folder)
   
4. Or use Git:
   ```bash
   git clone your_github_repo_url
   ```

### Step 3: Install Dependencies
1. Go to **Consoles** → Start a **Bash console**
2. Run:
   ```bash
   cd sdg-ethiopia-chatbot
   pip3 install --user -r requirements.txt
   ```

### Step 4: Run Bot Always
1. Go to **Tasks** tab
2. Create a new **Always-on task**
3. Command: 
   ```
   python3 /home/your_username/sdg-ethiopia-chatbot/telegram_bot.py
   ```
4. Click **Create**

### Step 5: Done!
- Bot is now running 24/7
- Will restart automatically if it crashes
- Check logs in the Tasks tab

---

## Alternative: Render.com (Also Free)

### Step 1: Create Account
1. Go to: https://render.com
2. Sign up (free)

### Step 2: Create New Web Service
1. Connect your GitHub repo
2. Or manually deploy

### Step 3: Configure
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python telegram_bot.py`
- Add environment variables from .env

### Step 4: Deploy
- Click "Create Web Service"
- Bot runs 24/7 automatically

---

## For Internship Demo

**Recommendation:** 
- Use PythonAnywhere for the internship period (1 month)
- It's free and reliable
- Show your supervisor the bot works 24/7
- After internship, ESS can deploy on their servers if they want

---

## Notes

- Free tiers have limits (usually enough for demos)
- PythonAnywhere free tier: Always-on task (perfect for Telegram bots)
- Keep your .env file secure (never commit to GitHub)
- Bot will work as long as the server runs
