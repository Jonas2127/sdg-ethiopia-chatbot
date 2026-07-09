# What to Run - Simple Guide

## 🎯 You Now Have 2 Options (That's It!)

### Option 1: Web Interface
```bash
streamlit run app.py
```
Opens in browser at http://localhost:8501

### Option 2: Telegram Bot
```bash
python telegram_bot.py
```
Works with Telegram app on your phone

---

## ✅ Both Include the Same Features:

- ✅ **UN Database** (11,346 stored documents)
- ✅ **World Bank API** (live, real-time)
- ✅ **ESS Website** (live scraping)

**No need to choose!** Both have everything.

---

## 🧪 Before Running: Test Everything

```bash
python test_unified_system.py
```

This checks:
- Python version
- Dependencies
- API keys
- Database
- Live fetching

---

## 📝 Quick Reference

### Commands You'll Use:

```bash
# 1. Test system (first time)
python test_unified_system.py

# 2. Run web app (most common)
streamlit run app.py

# 3. Run telegram bot (optional)
python telegram_bot.py

# 4. Install dependencies (if needed)
pip install -r requirements.txt
```

### That's literally all you need! 🎉

---

## ❓ Which One Should I Use?

### Use Web App (`app.py`) if you want:
- 🖥️ Desktop/laptop interface
- 📊 Visual statistics
- 🔍 Expandable source documents
- ⚙️ Settings controls
- 🗑️ Cache management button

### Use Telegram Bot (`telegram_bot.py`) if you want:
- 📱 Mobile access
- 💬 Chat interface
- 🚀 24/7 availability (deploy once, use forever)
- 🌐 Access from anywhere

### Use Both?
Sure! They work independently. Run web app for desktop, deploy Telegram bot for mobile.

---

## 🆘 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
➡️ Edit `.env` file and add your API key

### Error: "Collection not found"
➡️ Run: `python scripts/step7_build_vector_db.py`

### Error: "Module not found"
➡️ Run: `pip install -r requirements.txt`

### Telegram bot not responding?
➡️ Check `TELEGRAM_BOT_TOKEN` in `.env`

---

## 📚 Need More Help?

- **Quick Start**: `QUICK_START.md`
- **Full Guide**: `UNIFIED_SYSTEM_GUIDE.md`
- **What Changed**: `MIGRATION_SUMMARY.md`
- **Technical Details**: `docs/PROJECT_EXPLANATION.md`

---

## ✨ Remember

**Old way** (confusing):
```bash
python -m streamlit run app.py           # Only stored data
python -m streamlit run app_hybrid.py     # Stored + World Bank
python -m streamlit run app_fully_live.py # All sources
# Which one do I use??? 😵
```

**New way** (simple):
```bash
streamlit run app.py    # All sources included! ✅
```

---

**That's it! Just run `streamlit run app.py` and you're good to go! 🚀**
