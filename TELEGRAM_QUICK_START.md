# 🚀 Telegram Bot - Quick Start (5 Minutes)

Fast setup guide to get your Telegram bot running NOW.

---

## ⚡ Step 1: Create Bot (2 minutes)

1. Open Telegram → Search `@BotFather`
2. Send: `/newbot`
3. Name: `SDG Ethiopia Chatbot`
4. Username: `sdg_ethiopia_bot` (or any name ending in `bot`)
5. **Copy the token** BotFather gives you!

---

## 🖼️ Step 2: Add Logo (1 minute)

1. In BotFather, send: `/setuserpic`
2. Select your bot
3. Upload: `assets/sm_1684604849.312469.jpg`

---

## 🔑 Step 3: Add Token (1 minute)

1. Open `.env` file in your project
2. Add this line:
   ```
   TELEGRAM_BOT_TOKEN=paste_your_token_here
   ```
3. Save the file

---

## ▶️ Step 4: Run Bot (1 minute)

```cmd
pip install Pillow python-telegram-bot
python telegram_bot.py
```

You should see:
```
✅ Bot is running! Press Ctrl+C to stop.
```

---

## ✅ Step 5: Test It!

1. Open Telegram
2. Search for your bot: `@sdg_ethiopia_bot`
3. Send: `/start`
4. Ask: "What is Ethiopia's poverty rate?"

**Working?** 🎉 You're done!

**Not working?** See `TELEGRAM_BOT_SETUP.md` for detailed troubleshooting.

---

## 📱 Make It Better (Optional)

### Set Description
In BotFather, send: `/setdescription`

Then send:
```
Get instant access to Ethiopia's SDG data from UN, World Bank, and ESS. Ask about poverty, education, health, and more!
```

### Set Commands
In BotFather, send: `/setcommands`

Then send:
```
start - Welcome message
help - How to use
examples - Sample questions
stats - Bot statistics
```

---

## 🌐 Keep It Running 24/7

**Option 1: Leave Computer On**
- Keep terminal window open
- Bot stops when computer sleeps

**Option 2: PythonAnywhere (Free)**
- Sign up: https://pythonanywhere.com
- Upload project
- Create scheduled task

**Option 3: Cloud Service**
- Render.com (free)
- Heroku (paid)
- Railway.app (paid)

See `TELEGRAM_BOT_SETUP.md` for full deployment guide.

---

## 🆘 Quick Troubleshooting

### Bot doesn't start
```cmd
# Check if dependencies installed
pip install -r requirements.txt

# Check if ChromaDB exists
dir chroma_db
```

### Bot doesn't respond
- Check terminal for errors
- Verify token in `.env` (no quotes/spaces)
- Make sure Google API key is also in `.env`

### "Model not found" error
- Normal - bot will auto-detect available model
- Check if you see: "Using Gemini model: ..."

---

## 📞 Need Help?

Read the full guide: `TELEGRAM_BOT_SETUP.md`

Test your system: `python test_unified_system.py`

---

**That's it!** Your bot is live. Share it with users:

`https://t.me/your_bot_username`

🎉 **Congratulations!**
