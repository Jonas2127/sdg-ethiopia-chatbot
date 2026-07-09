# Complete Folder Structure Explained

## 📂 Every File and Folder - What It Does

```
sdg-ethiopia-chatbot/
│
├── 📄 .env
│   └─ YOUR SECRET KEYS (API tokens)
│      Keep this PRIVATE!
│
├── 📄 .env.example  
│   └─ Template (safe to share)
│
├── 📄 .gitignore
│   └─ List of files NOT to upload to GitHub
│
├── 📄 requirements.txt
│   └─ List of Python libraries to install
│
├── 📄 README.md
│   └─ Project description (first thing people see)
│
├── 🌐 app.py
│   └─ MAIN WEB APPLICATION
│      Run: python -m streamlit run app.py
│      → Opens chatbot in browser
│
├── 📱 telegram_bot.py
│   └─ TELEGRAM VERSION
│      Run: python telegram_bot.py
│      → Bot works on Telegram
│
├── 📁 assets/
│   ├── ess_logo.png          (original logo)
│   └── ess_logo_fixed.png    (circular, no background)
│
├── 📁 data/
│   │
│   ├── 📁 raw/              (Original downloaded data - DON'T EDIT!)
│   │   ├── worldbank_ethiopia_sdg.csv  (132 records from World Bank)
│   │   ├── un_sdg_ethiopia.csv         (11,903 records from UN)
│   │   └── 📁 un_sdg_raw/              (17 Excel files, one per SDG)
│   │       ├── Goal1.xlsx
│   │       ├── Goal2.xlsx
│   │       └── ... (up to Goal17.xlsx)
│   │
│   └── 📁 processed/        (Cleaned data - READY TO USE)
│       ├── ethiopia_sdg_clean.csv       (Combined clean dataset)
│       ├── worldbank_clean.csv          (World Bank only)
│       ├── un_sdg_clean.csv             (UN only)
│       └── 📁 knowledge_base/           (Text format for AI)
│           ├── documents.jsonl          (11,346 text documents)
│           ├── metadata.json            (Info about each document)
│           └── stats.json               (Summary statistics)
│
├── 📁 chroma_db/           (VECTOR DATABASE - AI's MEMORY)
│   └── [Database files]    
│       • Contains embeddings (vectors) for all documents
│       • Enables semantic search
│       • Created by step7_build_vector_db.py
│
├── 📁 scripts/             (SETUP SCRIPTS - Run once in order)
│   │
│   ├── step1_setup_test.py
│   │   └─ Tests if Python and libraries work
│   │      When: Day 1
│   │      Purpose: Verify installation
│   │
│   ├── step2_test_gemini.py
│   │   └─ Tests Gemini API connection
│   │      When: Day 1
│   │      Purpose: Confirm API key works
│   │
│   ├── step3_download_data.py
│   │   └─ Downloads data from World Bank
│   │      When: Day 2
│   │      Creates: data/raw/worldbank_ethiopia_sdg.csv
│   │
│   ├── step4_verify_data.py
│   │   └─ Checks if data files are valid
│   │      When: Day 2
│   │      Purpose: Confirm both datasets exist
│   │
│   ├── step4b_convert_excel_to_csv.py
│   │   └─ Converts 17 Excel files to one CSV
│   │      When: Day 2
│   │      Input: data/raw/un_sdg_raw/*.xlsx
│   │      Output: data/raw/un_sdg_ethiopia.csv
│   │
│   ├── step5_clean_data.py
│   │   └─ Cleans and merges all data
│   │      When: Day 3
│   │      - Removes missing values
│   │      - Standardizes column names
│   │      - Combines World Bank + UN data
│   │      Output: data/processed/ethiopia_sdg_clean.csv
│   │
│   ├── step6_create_knowledge_base.py
│   │   └─ Converts data to text documents
│   │      When: Day 4
│   │      - Creates 11,346 readable documents
│   │      - Adds context to each data point
│   │      Output: data/processed/knowledge_base/
│   │
│   ├── step7_build_vector_db.py
│   │   └─ Creates vector database
│   │      When: Day 5
│   │      - Generates embeddings (384 dimensions)
│   │      - Stores in ChromaDB
│   │      Output: chroma_db/
│   │
│   ├── step8_build_chatbot.py
│   │   └─ Tests chatbot logic
│   │      When: Day 6
│   │      - Tests RAG system
│   │      - Tries sample questions
│   │
│   └── fix_logo.py
│       └─ Removes white background from logo
│          When: Anytime (for UI improvement)
│          Output: assets/ess_logo_fixed.png
│
└── 📁 docs/                (DOCUMENTATION)
    ├── DAILY_LOG.md
    │   └─ Day-by-day progress tracker
    │
    ├── DATA_SOURCES.md
    │   └─ Where data comes from + how to download
    │
    ├── DEPLOY_TELEGRAM_BOT.md
    │   └─ How to deploy bot 24/7 (PythonAnywhere)
    │
    ├── PROJECT_EXPLANATION.md
    │   └─ Complete logic explanation (you're reading related doc!)
    │
    └── FOLDER_STRUCTURE.md
        └─ This file!
```

---

## 🎯 FILE CATEGORIES

### **🔑 Configuration (DON'T TOUCH after setup)**
- `.env` - Your secrets
- `.gitignore` - Git settings
- `requirements.txt` - Dependencies list

### **🚀 Applications (RUN THESE)**
- `app.py` - Web chatbot
- `telegram_bot.py` - Telegram chatbot

### **📊 Data (READ-ONLY after creation)**
- `data/raw/` - Original data
- `data/processed/` - Clean data
- `chroma_db/` - Vector database

### **🖼️ Assets (CUSTOMIZE)**
- `assets/` - Logos and images

### **🛠️ Scripts (RUN ONCE in order)**
- `scripts/step1` through `step8`
- Setup and data processing

### **📖 Documentation (READ for understanding)**
- `docs/` - All explanations

---

## 🔄 WORKFLOW SUMMARY

```
1. SETUP (Day 1)
   scripts/step1_setup_test.py
   scripts/step2_test_gemini.py
   
2. DATA COLLECTION (Day 2)
   scripts/step3_download_data.py
   Manual: Download UN data
   scripts/step4b_convert_excel_to_csv.py
   scripts/step4_verify_data.py
   
3. DATA PROCESSING (Day 3-5)
   scripts/step5_clean_data.py
   scripts/step6_create_knowledge_base.py
   scripts/step7_build_vector_db.py
   
4. TESTING (Day 6)
   scripts/step8_build_chatbot.py
   
5. RUN CHATBOT (Day 7+)
   python -m streamlit run app.py
   OR
   python telegram_bot.py
```

---

## 💾 FILE SIZES (Approximate)

```
Small (< 1 MB):
- All .py files
- .env, .gitignore, requirements.txt
- Documentation files

Medium (1-10 MB):
- data/processed/ethiopia_sdg_clean.csv (~1.3 MB)
- data/processed/knowledge_base/documents.jsonl (~4 MB)

Large (10-100 MB):
- chroma_db/ (~50 MB)
  Contains embeddings for 11,346 documents

Very Large (100+ MB):
- Model cache (first time download)
  SentenceTransformer models (~400 MB)
  Downloaded automatically when needed
```

---

## 🗑️ What You CAN Delete (if needed)

**After successful deployment:**
- `scripts/` folder (setup scripts no longer needed)
- `data/raw/` folder (keep processed data only)
- `docs/DAILY_LOG.md` (personal notes)

**NEVER Delete:**
- `.env` (your keys!)
- `app.py` or `telegram_bot.py` (the actual chatbot)
- `chroma_db/` (the AI's memory)
- `data/processed/` (clean data)
- `requirements.txt` (needed for deployment)

---

## 🎓 FOR YOUR INTERNSHIP PRESENTATION

**Show these folders to demonstrate your work:**

1. **data/raw/** → "I collected data from UN and World Bank"
2. **data/processed/** → "I cleaned and organized 11,346 records"
3. **chroma_db/** → "I built a vector database for semantic search"
4. **app.py** → "I created a web interface with Streamlit"
5. **telegram_bot.py** → "I made it work on Telegram too"
6. **docs/** → "I documented everything professionally"

This shows: data engineering, AI/ML, full-stack development, and documentation!

---

**Any specific file or folder you want me to explain in more detail?**
