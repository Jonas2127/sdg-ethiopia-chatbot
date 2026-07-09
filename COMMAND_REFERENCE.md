# Command Reference Card - Quick Copy/Paste

## 🚀 Essential Commands (Copy & Paste)

### Test System
```bash
python test_unified_system.py
```

### Run Web App
```bash
streamlit run app.py
```

### Run Telegram Bot
```bash
python telegram_bot.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔄 Update Stored Data (Quarterly)

### Full Update Pipeline
```bash
# Step 1: Download new data
python scripts/step3_download_data.py

# Step 2: Clean the data
python scripts/step5_clean_data.py

# Step 3: Create knowledge base
python scripts/step6_create_knowledge_base.py

# Step 4: Rebuild vector database
python scripts/step10_rebuild_vector_db.py
```

### Quick Update (One-liner)
```bash
python scripts/step3_download_data.py & python scripts/step5_clean_data.py & python scripts/step6_create_knowledge_base.py & python scripts/step10_rebuild_vector_db.py
```

---

## 📄 Process New ESS Reports

```bash
# Step 1: Process ESS PDF reports
python scripts/step9_process_ess_reports.py

# Step 2: Rebuild vector database
python scripts/step10_rebuild_vector_db.py
```

---

## 🧪 Testing Commands

### Test Environment
```bash
python scripts/step1_setup_test.py
```

### Test Gemini API
```bash
python scripts/step2_test_gemini.py
```

### Test Complete System
```bash
python test_unified_system.py
```

---

## 📂 Data Management

### Check Database
```bash
# In Python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="ethiopia_sdg")
print(f"Documents: {collection.count()}")
```

### Clear Cache
```bash
# Windows
rmdir /s /q cache

# Then recreate (or app will do it automatically)
mkdir cache
```

### View Cache Contents
```bash
# Windows
dir cache
```

---

## 🌐 Git Commands (If Using Version Control)

### Initial Commit
```bash
git add .
git commit -m "Unified SDG Ethiopia Chatbot v2.0"
git push
```

### Update After Changes
```bash
git add .
git commit -m "Update: [describe your changes]"
git push
```

### Check Status
```bash
git status
```

---

## 📊 Check Data Statistics

### Count Documents in ChromaDB
```bash
python -c "import chromadb; client = chromadb.PersistentClient(path='./chroma_db'); print(f'Documents: {client.get_collection(name=\"ethiopia_sdg\").count()}')"
```

### Check Cache Size
```bash
dir cache /s
```

### Check Data Files
```bash
dir data\raw /s
dir data\processed /s
```

---

## 🔐 Environment Configuration

### Check .env File
```bash
type .env
```

### Edit .env File
```bash
notepad .env
```

### Required Keys in .env:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

---

## 🚑 Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Installed Packages
```bash
pip list
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Force Reinstall
```bash
pip install -r requirements.txt --force-reinstall
```

### Check Streamlit
```bash
streamlit --version
```

### Check ChromaDB
```bash
python -c "import chromadb; print(chromadb.__version__)"
```

---

## 🧹 Cleanup Commands

### Remove Cache
```bash
rmdir /s /q cache
```

### Remove ChromaDB (WARNING: Deletes all stored data!)
```bash
# Only if you want to rebuild from scratch
rmdir /s /q chroma_db
```

### Remove Python Cache
```bash
# Clean __pycache__ directories
for /d /r %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d"
```

---

## 📱 Telegram Bot Commands

### Once Bot is Running:

In Telegram app, send these commands:

```
/start     - Welcome message
/help      - Usage instructions
/examples  - Example questions
/stats     - Bot statistics
```

### Example Questions to Ask:
```
What is Ethiopia's poverty rate?
Show me education statistics
Latest health indicators
```

---

## 🎯 Development Workflow

### Daily Use:
```bash
streamlit run app.py
```

### After Updating Code:
```bash
# Stop app (Ctrl+C)
# Restart app
streamlit run app.py
```

### After Updating Data:
```bash
# Run update pipeline (see above)
# Then restart app
streamlit run app.py
```

---

## 📦 Package Management

### Export Current Environment
```bash
pip freeze > requirements_current.txt
```

### Install from requirements
```bash
pip install -r requirements.txt
```

### Update Single Package
```bash
pip install --upgrade package_name
```

### Check Outdated Packages
```bash
pip list --outdated
```

---

## 🔍 Debugging Commands

### Run with Verbose Output
```bash
streamlit run app.py --logger.level=debug
```

### Check for Errors in Scripts
```bash
python -m py_compile unified_data_fetcher.py
python -m py_compile app.py
python -m py_compile telegram_bot.py
```

### Test Data Fetcher Directly
```bash
python -c "from unified_data_fetcher import UnifiedDataFetcher; f = UnifiedDataFetcher(); print(f.fetch_worldbank_indicator('SI.POV.DDAY'))"
```

---

## 🌐 Network Testing

### Test World Bank API
```bash
curl "https://api.worldbank.org/v2/country/ETH/indicator/SI.POV.DDAY?format=json&per_page=1"
```

### Test ESS Website
```bash
curl "https://www.statsethiopia.gov.et"
```

### Check Internet Connection
```bash
ping google.com
```

---

## 📊 Performance Testing

### Time a Query
```bash
python -c "import time; from unified_data_fetcher import UnifiedDataFetcher; f = UnifiedDataFetcher(); start = time.time(); f.fetch_all_sources('poverty'); print(f'Time: {time.time()-start:.2f}s')"
```

### Check Memory Usage
```bash
# While app is running, in Task Manager:
# Find "python.exe" processes
```

---

## 🎓 Learning Commands

### Explore ChromaDB Structure
```bash
python
>>> import chromadb
>>> client = chromadb.PersistentClient(path="./chroma_db")
>>> collection = client.get_collection(name="ethiopia_sdg")
>>> print(f"Count: {collection.count()}")
>>> # Get a sample document
>>> result = collection.get(limit=1)
>>> print(result)
>>> exit()
```

### Test Embeddings
```bash
python
>>> from sentence_transformers import SentenceTransformer
>>> model = SentenceTransformer('all-MiniLM-L6-v2')
>>> embedding = model.encode("What is poverty?")
>>> print(f"Embedding dimension: {len(embedding)}")
>>> exit()
```

---

## 🚀 Deployment Commands

### For Streamlit Cloud:
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Connect to Streamlit Cloud
# 3. Deploy app.py
```

### For PythonAnywhere (Telegram Bot):
```bash
# 1. Upload files via Files tab
# 2. Install requirements in Bash console
pip install -r requirements.txt

# 3. Run bot
python telegram_bot.py
```

---

## 💡 Quick Tips

### Open Multiple Terminals:
```bash
# Terminal 1: Web app
streamlit run app.py

# Terminal 2: Telegram bot (in new window)
python telegram_bot.py
```

### Check Logs:
```bash
# Streamlit creates logs in:
# C:\Users\[YourUser]\.streamlit\logs\
```

### Quick Data Refresh:
```bash
# Just rebuild vector DB from existing knowledge base
python scripts/step10_rebuild_vector_db.py
```

---

## 📋 Common Workflows

### First Time Setup:
```bash
pip install -r requirements.txt
python test_unified_system.py
streamlit run app.py
```

### Daily Use:
```bash
streamlit run app.py
```

### Data Update (Quarterly):
```bash
python scripts/step3_download_data.py
python scripts/step5_clean_data.py
python scripts/step6_create_knowledge_base.py
python scripts/step10_rebuild_vector_db.py
streamlit run app.py
```

### Adding ESS Reports:
```bash
# 1. Put PDFs in data/raw/ess/
python scripts/step9_process_ess_reports.py
python scripts/step10_rebuild_vector_db.py
streamlit run app.py
```

---

## 🎯 One-Liner Commands

### Complete Test & Run:
```bash
python test_unified_system.py && streamlit run app.py
```

### Update Data & Run:
```bash
python scripts/step3_download_data.py && python scripts/step5_clean_data.py && python scripts/step6_create_knowledge_base.py && python scripts/step10_rebuild_vector_db.py && streamlit run app.py
```

### Check Everything:
```bash
python --version && pip list && python test_unified_system.py
```

---

**Save this file for quick reference!** 📌

All commands are tested and ready to copy/paste into your terminal.
