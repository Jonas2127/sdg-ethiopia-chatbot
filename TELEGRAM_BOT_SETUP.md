# 🤖 Telegram Bot Setup Guide

Complete guide to setting up your SDG Ethiopia Chatbot on Telegram with the ESS logo.

---

## 📱 Step 1: Create Your Telegram Bot

### 1.1 Find BotFather

1. Open **Telegram** (mobile or desktop)
2. Search for: **@BotFather**
3. Click **Start** or send `/start`

### 1.2 Create the Bot

1. Send command:
   ```
   /newbot
   ```

2. **Choose a name** (display name):
   ```
   SDG Ethiopia Chatbot
   ```

3. **Choose a username** (must end with `bot`):
   ```
   sdg_ethiopia_bot
   ```
   
   If taken, try alternatives:
   - `sdg_eth_statistics_bot`
   - `ethiopia_sdg_data_bot`
   - `ess_ethiopia_bot`
   - `eth_development_bot`

4. **Success!** BotFather gives you a **token**:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567
   ```
   
   ⚠️ **SAVE THIS TOKEN!** You need it in Step 3.

---

## 🖼️ Step 2: Set the ESS Logo

### 2.1 Upload Profile Picture

1. In BotFather chat, send:
   ```
   /setuserpic
   ```

2. Select your bot from the list

3. Upload the logo image:
   - **File location:** `assets/sm_1684604849.312469.jpg`
   - **On phone:** Camera icon → Select from gallery
   - **On desktop:** Paperclip icon → Upload file

4. ✅ Done! Your bot now has the ESS logo

### 2.2 Set Bot Description (Optional but Recommended)

Make your bot more professional:

**About Text** (shows in profile):
```
/setabouttext
```
Select your bot, then send:
```
Official SDG Ethiopia Chatbot providing real-time Ethiopian statistics and development indicators from UN, World Bank, and ESS.
```

**Description** (shows in chat):
```
/setdescription
```
Select your bot, then send:
```
I provide instant access to Ethiopia's Sustainable Development Goals data. Ask me about poverty, education, health, infrastructure, environment, and more! 

Data sources:
🌍 World Bank API
🇪🇹 Ethiopian Statistical Service
🔵 UN SDG Database

Just send me your question!
```

**Commands Menu**:
```
/setcommands
```
Select your bot, then send:
```
start - Welcome message and overview
help - How to use the bot
examples - Example questions to ask
stats - Bot statistics and status
```

---

## 🔐 Step 3: Configure Bot Token

1. Open your `.env` file in the project folder

2. Add your bot token (from Step 1):
   ```env
   GOOGLE_API_KEY=your_existing_google_api_key
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567
   ```

3. **Save** the file

---

## 🚀 Step 4: Run the Bot

### 4.1 Install Dependencies (if not done)

```cmd
pip install python-telegram-bot
```

Or install all dependencies:
```cmd
pip install -r requirements.txt
```

### 4.2 Start the Bot

```cmd
python telegram_bot.py
```

You should see:
```
🚀 Starting SDG Ethiopia Telegram Bot...
Loading embedding model...
Connecting to ChromaDB...
Initializing Gemini API...
Available Gemini models: [...]
Using Gemini model: models/gemini-x.x-flash
Initializing unified data fetcher...
✅ All components initialized successfully!
✅ Bot is running! Press Ctrl+C to stop.
```

### 4.3 Test Your Bot

1. Open Telegram
2. Search for your bot: `@sdg_ethiopia_bot` (or your username)
3. Click **Start**
4. Try these commands:
   - `/start` - Welcome message
   - `/help` - Usage guide
   - `/examples` - Example questions
   - `/stats` - Bot statistics

5. Ask a question:
   - "What is Ethiopia's poverty rate?"
   - "Show education enrollment trends"
   - "Latest child mortality data"

---

## 🎯 Bot Commands Reference

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with overview |
| `/help` | How to use the bot |
| `/examples` | Sample questions by category |
| `/stats` | Bot statistics and system status |

---

## 🌐 Step 5: Keep Bot Running 24/7 (Optional)

Your bot only works when `telegram_bot.py` is running. To keep it online 24/7:

### Option A: Run on Local Computer (Simple)

**Keep terminal open:**
```cmd
python telegram_bot.py
```

⚠️ Bot stops when you close terminal or computer sleeps.

### Option B: PythonAnywhere (Free, Recommended)

1. **Sign up:** https://www.pythonanywhere.com (free account)

2. **Upload your project:**
   - Zip your project folder
   - Upload to PythonAnywhere
   - Extract files

3. **Install dependencies:**
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Create scheduled task:**
   - Go to "Tasks" tab
   - Add: `python /home/yourusername/telegram_bot.py`
   - Set to run daily (will keep restarting)

5. **Or use Always-On task** (paid):
   - Upgrade to paid account
   - Create "Always-on task"
   - Add `python telegram_bot.py`

### Option C: Render (Free)

1. **Sign up:** https://render.com

2. **Create new Web Service:**
   - Connect your GitHub repo
   - Or upload project

3. **Configure:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python telegram_bot.py
   ```

4. **Add environment variables:**
   - `GOOGLE_API_KEY`: Your key
   - `TELEGRAM_BOT_TOKEN`: Your token

5. **Deploy!**

### Option C: Heroku

1. **Sign up:** https://heroku.com

2. **Install Heroku CLI**

3. **Deploy:**
   ```cmd
   heroku login
   heroku create sdg-ethiopia-bot
   git push heroku main
   heroku config:set GOOGLE_API_KEY=your_key
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   ```

---

## 🔧 Troubleshooting

### Bot doesn't respond

**Check if bot is running:**
```cmd
python telegram_bot.py
```

Should show: `✅ Bot is running!`

**Check token:**
- Open `.env`
- Verify `TELEGRAM_BOT_TOKEN` is correct
- No spaces or quotes

### "Gemini API error"

**Check Google API key:**
- Open `.env`
- Verify `GOOGLE_API_KEY` is correct
- Test with: `python test_unified_system.py`

### "ChromaDB not found"

**Build the database first:**
```cmd
python scripts/step7_build_vector_db.py
```

### Bot sends error messages

**Check logs in terminal:**
- Look for error messages
- Common issues:
  - API key invalid
  - ChromaDB not initialized
  - Network connection issues

### Bot is slow

**Normal behavior:**
- First response: 5-10 seconds (loading models)
- Subsequent: 2-5 seconds (fetching live data)

**Speed up:**
- Reduce `n_results` in `telegram_bot.py` (line 133)
- Disable live data fetching for testing

---

## 📊 Bot Features

### Data Sources
- 🌍 **World Bank API** - Real-time economic indicators
- 🇪🇹 **ESS Website** - Latest Ethiopian statistics
- 🔵 **UN SDG Database** - Sustainable Development Goals
- 📁 **11,346 stored documents** - Historical data

### Capabilities
- ✅ Natural language questions
- ✅ Real-time data fetching
- ✅ Historical trend analysis
- ✅ Source citation
- ✅ Multi-source comparison
- ✅ Markdown formatting

### Response Format
```
📝 Answer:
[AI-generated answer with data]

---
📊 Sources: 12 stored + 5 live
🌐 Live Data: 🌍 World Bank: 3 | 🇪🇹 ESS: 2 | 🔵 UN: checked
```

---

## 🎨 Customization

### Change Bot Personality

Edit the prompt in `telegram_bot.py` (line 193-212):
```python
prompt = f"""You are an expert assistant on Ethiopia's SDGs.

Guidelines:
- Be friendly and professional
- Use emojis for clarity
- Keep responses concise
...
```

### Add More Commands

Add handler in `telegram_bot.py` (line 426):
```python
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your custom response")

application.add_handler(CommandHandler("custom", custom_command))
```

### Modify Response Length

Change truncation limit (line 233):
```python
if len(answer) > 4000:  # Change this number
    answer = answer[:4000] + "\n\n...(truncated)"
```

---

## 📞 Support

### Need Help?

1. **Check logs:** Look at terminal output for errors
2. **Test system:** Run `python test_unified_system.py`
3. **Review documentation:**
   - `README.md` - Project overview
   - `QUICK_START.md` - Quick setup guide
   - `docs/TROUBLESHOOTING.md` - Common issues

### Common Questions

**Q: Can users see each other's questions?**
A: No. Each chat is private.

**Q: How many users can use the bot?**
A: Unlimited. Each user has independent sessions.

**Q: Does it work in groups?**
A: Yes! Add the bot to a Telegram group.

**Q: Can I customize the responses?**
A: Yes. Edit the prompt in `telegram_bot.py`.

**Q: How much does it cost?**
A: Free if you host locally. Cloud hosting varies ($0-$10/month).

---

## ✅ Checklist

Before going live:

- [ ] Bot token added to `.env`
- [ ] Google API key configured
- [ ] ChromaDB built (`step7_build_vector_db.py`)
- [ ] ESS logo uploaded
- [ ] Bot description set
- [ ] Commands menu configured
- [ ] Tested `/start`, `/help`, `/stats`
- [ ] Tested sample questions
- [ ] Decided on hosting method
- [ ] Bot running 24/7 (if needed)

---

## 🎉 You're Done!

Your SDG Ethiopia Chatbot is now live on Telegram! 🚀

Users can find it by searching: `@your_bot_username`

Share your bot:
- Send link: `https://t.me/your_bot_username`
- QR code: Get from Telegram settings
- Direct share: Forward bot contact

---

**Need more help?** Check other documentation files:
- `QUICK_START.md` - Overall setup guide
- `docs/PROJECT_EXPLANATION.md` - How it works
- `docs/TROUBLESHOOTING.md` - Fix common issues
