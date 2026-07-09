# Quick Start Guide - SDG Ethiopia Chatbot v2.0

## 🎯 What Data Does the Chatbot Use?

### BOTH Stored AND Live Data! 🎉

**Every query uses:**
1. � **Stored Data** (11,346 documents in ChromaDB)
   - UN SDG Database (downloaded)
   - World Bank historical data (downloaded)
   - ESS reports (downloaded PDFs)
   
2. 🌐 **Live Data** (fetched in real-time)
   - World Bank API (latest indicators)
   - ESS Website (current publications)

**Result**: You get comprehensive historical coverage PLUS the latest updates!

---

## �🚀 Get Running in 3 Steps

### Step 1: Test Your System
```bash
python test_unified_system.py
```

This will check:
- ✅ Python version
- ✅ Required files
- ✅ Dependencies installed
- ✅ API keys configured
- ✅ Database ready (11,346 stored documents)
- ✅ Data fetcher working (live sources)

### Step 2: Run the Web App
```bash
streamlit run app.py
```

Open browser at: http://localhost:8501

### Step 3: Try These Questions

**Poverty:**
```
What is Ethiopia's poverty rate?
```

**Education:**
```
Show me primary school enrollment trends
```

**Health:**
```
What is the child mortality rate in Ethiopia?
```

You'll see the chatbot uses BOTH stored documents AND live data!

---

## 📱 Want the Telegram Bot?

### 1. Get a Bot Token

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions
5. Copy the token

### 2. Add Token to .env

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. Run the Bot

```bash
python telegram_bot.py
```

---

## 🛠️ First Time Setup

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Configure .env:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token  # Optional
```

Get Google API key: https://ai.google.dev/

---

## 🌐 Data Sources Explained

### Stored Data (ChromaDB - 11,346 docs):
✅ **UN SDG Database** - Historical data (1995-2026)  
✅ **World Bank** - Downloaded historical indicators  
✅ **ESS Reports** - Processed PDF documents  
- **Updated by**: Running scripts (step3→step5→step6→step7)
- **Used in**: Every query (always searched first)

### Live Data (Real-time fetching):
✅ **World Bank API** - Latest indicators  
✅ **ESS Website** - Current publications  
- **Updated by**: Automatic! Every query
- **Used in**: Every query (fetched after stored search)

**Both systems work together for comprehensive answers!**

---

## ⚙️ Web App Features

### Sidebar:
- **Fetch Live Data** checkbox - Toggle real-time fetching
- **Clear Cache** button - Force fresh data
- **Example Questions** - Copy and paste to try

### Main Interface:
- Type your question
- Click "🔍 Search"
- Get answer with source statistics
- View raw sources (expandable)

---

## 💡 Tips for Best Results

✅ **Be specific**: "poverty rate in 2024" vs. "poverty"  
✅ **Ask about trends**: "how has X changed over time"  
✅ **Request comparisons**: "compare rural vs urban"  
✅ **Mention years**: "from 2010 to 2024"  

---

## 🔧 Troubleshooting

### "No GOOGLE_API_KEY found"
➡️ Add it to `.env` file

### "Collection not found"
➡️ Run: `python scripts/step7_build_vector_db.py`

### "Rate limit exceeded"
➡️ Wait 1 hour or click "Clear Cache"

### "ESS website error"
➡️ Website may be down (temporary), system uses stored data

---

## 📊 Response Time

- **Fast mode** (stored only): 3-4 seconds
- **Live mode** (all sources): 7-10 seconds

Caching makes repeated questions faster!

---

## 📚 More Help

- **Full guide**: `UNIFIED_SYSTEM_GUIDE.md`
- **Technical docs**: `docs/PROJECT_EXPLANATION.md`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`

---

## ✅ Checklist

Before running:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file has `GOOGLE_API_KEY`
- [ ] ChromaDB exists (`chroma_db/` folder)
- [ ] Test passed (`python test_unified_system.py`)

Ready to run:
- [ ] `streamlit run app.py` → Web interface
- [ ] `python telegram_bot.py` → Telegram bot

---

**That's it! You're ready to use the unified SDG Ethiopia Chatbot. 🎉**
