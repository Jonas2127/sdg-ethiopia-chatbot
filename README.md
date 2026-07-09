# SDG Ethiopia Chatbot 🇪🇹

**Unified Live Data System - Version 2.0**

An intelligent conversational interface for Ethiopia's Sustainable Development Goals with **real-time updates** from UN, World Bank, and ESS.

---

## 🎯 Quick Start

### Run the Web App:
```bash
streamlit run app.py
```

### Run the Telegram Bot:
```bash
python telegram_bot.py
```

**That's it!** No more confusion with multiple app versions. Everything is unified.

---

## ✨ What's New in v2.0?

### Before (v1.x - Confusing):
- ❌ 3 different apps: `app.py`, `app_hybrid.py`, `app_fully_live.py`
- ❌ 2 different fetchers: `live_data_fetcher.py`, `ess_live_fetcher.py`
- ❌ Had to choose which version to run
- ❌ Unclear data sources for each version

### After (v2.0 - Simple):
- ✅ **1 web app**: `streamlit run app.py`
- ✅ **1 Telegram bot**: `python telegram_bot.py`
- ✅ **1 unified fetcher**: `unified_data_fetcher.py`
- ✅ **All 3 data sources** active in every query:
  - 🌍 World Bank API (live)
  - 🇪🇹 ESS Website (live scraping)
  - 🔵 UN SDG Database (11,346 stored docs)
- ✅ **Auto-updates** when new data is available
- ✅ **Smart caching** (6 hours) to avoid rate limits

---

## 🌐 Data Sources

### 1. World Bank API 🌍
- **Status**: Live fetching enabled
- **Update frequency**: Real-time
- **Rate limit**: 1,500 requests/day (free tier)
- **Cached for**: 6 hours
- **Coverage**: Economic and social indicators

### 2. ESS Website 🇪🇹
- **Status**: Live scraping enabled
- **URL**: https://www.statsethiopia.gov.et
- **Update frequency**: Fetches latest publications
- **Cached for**: 6 hours
- **Coverage**: National surveys, census, bulletins

### 3. UN SDG Database 🔵
- **Status**: 11,346 documents stored locally
- **Update frequency**: Quarterly (manual download)
- **Coverage**: All 17 SDGs, 231 indicators
- **Years**: 1995-2026

---

## 📊 Features

### Web App (`app.py`):
- ✅ Real-time data from 3 sources
- ✅ 11,346 historical documents
- ✅ Smart keyword detection
- ✅ Source statistics (stored vs. live)
- ✅ Cache management
- ✅ Expandable source documents
- ✅ Mobile-responsive design

### Telegram Bot (`telegram_bot.py`):
- ✅ Same data sources as web app
- ✅ Commands: `/start`, `/help`, `/examples`, `/stats`
- ✅ Typing indicators
- ✅ Mobile-optimized responses
- ✅ Source count in footer

---

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd sdg-ethiopia-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create/edit `.env` file:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token  # Optional for Telegram bot
```

**Get API Keys:**
- **Google Gemini**: https://ai.google.dev/
- **Telegram Bot**: Search `@BotFather` on Telegram

### 4. Run the App
```bash
# Web interface
streamlit run app.py

# OR Telegram bot
python telegram_bot.py
```

---

## 💡 Example Questions

### Poverty & Economy:
- What is Ethiopia's current poverty rate?
- How has GDP per capita changed?
- Show me income inequality trends

### Education:
- What is the primary school enrollment rate?
- How has literacy improved over time?
- Gender gap in education statistics

### Health:
- What is the current child mortality rate?
- How has life expectancy changed?
- Latest infant mortality statistics

### Infrastructure:
- What percentage has access to electricity?
- Clean water access statistics
- Sanitation coverage in Ethiopia

### Environment:
- How much forest coverage does Ethiopia have?
- Deforestation trends over time
- Environmental indicators for Ethiopia

---

## 📁 Project Structure

```
sdg-ethiopia-chatbot/
│
├── unified_data_fetcher.py    # ⭐ Unified fetcher (UN + World Bank + ESS)
├── app.py                      # ⭐ Streamlit web interface
├── telegram_bot.py             # ⭐ Telegram bot interface
├── requirements.txt            # Dependencies
├── .env                        # API keys (create this)
│
├── chroma_db/                  # Vector database (11,346 docs)
├── data/                       # Raw and processed data
├── cache/                      # Auto-created cache folder
├── scripts/                    # Setup scripts (one-time use)
└── docs/                       # Documentation
```

### Key Files:
- **`unified_data_fetcher.py`**: Single fetcher for all 3 data sources
- **`app.py`**: Main web interface (replaces 3 old versions)
- **`telegram_bot.py`**: Telegram interface (updated for unified system)

---

## 🔧 How It Works

### Data Flow:
```
User Question
    ↓
1. Search Stored Database (ChromaDB)
   └─ Retrieve 12 relevant documents
    ↓
2. Fetch Live Data (Parallel)
   ├─ World Bank API (2 indicators)
   ├─ ESS Website (scrape publications)
   └─ UN Database (status check)
    ↓
3. Combine All Sources
   └─ Stored + Live data
    ↓
4. Generate Answer (Gemini AI)
   └─ Cites most recent sources
    ↓
Answer + Source Statistics
```

### Smart Features:
- **Keyword Detection**: Automatically detects topics (poverty, education, health) and fetches relevant indicators
- **Caching**: 6-hour cache prevents rate limit issues
- **Fallback**: If live data fails, uses stored data automatically
- **Source Prioritization**: Newest data is prioritized in answers

---

## 📈 Performance

### Response Times:
- **Stored data only**: 3-4 seconds
- **With live fetching**: 7-10 seconds
  - Database search: ~1 second
  - Live data fetch: ~4-5 seconds
  - AI generation: ~2-3 seconds

### Optimization:
- ✅ 6-hour caching (reduces API calls)
- ✅ Parallel fetching (not sequential)
- ✅ Limited to 2 keywords per query
- ✅ Smart keyword detection

---

## 🛠️ Troubleshooting

### No live data fetched?
1. Check internet connection
2. Verify `.env` has `GOOGLE_API_KEY`
3. Clear cache (click button in web app)
4. Check if ESS website is accessible

### Rate limit error (World Bank)?
- Free tier: 1,500 requests/day
- Wait 1 hour for cache to expire
- System uses cache automatically

### ESS website scraping fails?
- ESS website may be temporarily down
- System falls back to stored data
- Check: https://www.statsethiopia.gov.et

### Gemini AI error (503)?
- Automatic retry (3 attempts)
- Wait a few seconds and try again
- Check API key is valid

---

## 📚 Documentation

- **[UNIFIED_SYSTEM_GUIDE.md](UNIFIED_SYSTEM_GUIDE.md)** - Complete guide for the new system
- **[PROJECT_EXPLANATION.md](docs/PROJECT_EXPLANATION.md)** - Technical details
- **[FOLDER_STRUCTURE.md](docs/FOLDER_STRUCTURE.md)** - Directory structure
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues

---

## 🎓 Technical Stack

### AI & ML:
- **LLM**: Google Gemini 2.0 Flash Exp
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB

### Data Sources:
- **World Bank API**: REST API with JSON responses
- **ESS Website**: BeautifulSoup web scraping
- **UN SDG Database**: Downloaded CSV files

### Frameworks:
- **Web**: Streamlit
- **Bot**: python-telegram-bot
- **HTTP**: requests library

---

## 📊 Database Statistics

- **Total Documents**: 11,346
- **Unique Indicators**: 465
- **Year Range**: 1995-2026
- **All 17 SDGs**: ✅
- **231 UN Indicators**: ✅
- **Vector Dimensions**: 384

---

## 🚀 Deployment

### Web App (Streamlit Community Cloud):
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets (API keys)
4. Deploy `app.py`

### Telegram Bot (24/7 hosting):
1. Use PythonAnywhere (free tier)
2. Upload files
3. Configure `.env`
4. Run `python telegram_bot.py` in console

---

## 🔐 Security

- ✅ API keys in `.env` (not committed to Git)
- ✅ `.gitignore` includes sensitive files
- ✅ No hardcoded credentials
- ✅ Rate limiting respected

---

## 📝 Version History

### v2.0 (Current) - Unified Live System
- Simplified to 1 app per interface
- Unified data fetcher for all 3 sources
- Auto-caching and auto-updates
- Removed confusing multiple versions

### v1.x - Original System
- Multiple app versions
- Separate fetchers
- Manual selection of data sources

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Submit a pull request

---

## 📞 Support

For issues or questions:
1. Check `UNIFIED_SYSTEM_GUIDE.md`
2. Review error messages in console
3. Verify `.env` configuration
4. Test individual data sources

---

## 📄 License

This project is for educational and research purposes.

---

## 🙏 Acknowledgments

- **UN SDG Database**: https://unstats.un.org/sdgs/dataportal/
- **World Bank Open Data**: https://data.worldbank.org/
- **Ethiopian Statistical Service**: https://www.statsethiopia.gov.et/
- **Google Gemini AI**: https://ai.google.dev/

---

**Version**: 2.0 - Unified Live System  
**Status**: Production Ready ✅  
**Last Updated**: 2026-07-08
