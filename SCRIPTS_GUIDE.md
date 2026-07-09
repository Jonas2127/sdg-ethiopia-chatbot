# Scripts Guide - What to Keep, Delete, or Modify

## 🎯 Quick Answer

### ✅ KEEP (Useful for maintaining data):
- `step3_download_data.py` - Download new UN/World Bank data
- `step5_clean_data.py` - Clean downloaded data
- `step6_create_knowledge_base.py` - Process data into documents
- `step7_build_vector_db.py` - Build/rebuild ChromaDB
- `step9_process_ess_reports.py` - Process ESS PDF reports
- `step10_rebuild_vector_db.py` - Rebuild database when needed

### ⚠️ OPTIONAL (Testing utilities):
- `step1_setup_test.py` - Test Python setup
- `step2_test_gemini.py` - Test Gemini API
- `step4_verify_data.py` - Verify downloaded data
- `step4b_convert_excel_to_csv.py` - Convert Excel to CSV

### ❌ DELETE (Obsolete):
- `step8_build_chatbot.py` - Old chatbot builder (replaced by unified system)
- `fix_logo.py` - Utility script (one-time use)

---

## 📊 How the Data Flow Works

### Initial Setup (One-Time):
```
Step 3: Download Data
   ↓
Step 4: Verify Data (optional)
   ↓
Step 5: Clean Data
   ↓
Step 6: Create Knowledge Base
   ↓
Step 7: Build Vector Database (ChromaDB)
   ↓
✅ Ready to use chatbot!
```

### Running the Chatbot:
```
User asks question
   ↓
1. Search ChromaDB (downloaded data)
   ↓
2. Fetch live data (World Bank + ESS)
   ↓
3. Combine both sources
   ↓
4. Generate answer
```

### When to Update Data (Optional):
```
Step 3: Download new UN/World Bank data (quarterly)
   ↓
Step 5: Clean new data
   ↓
Step 6: Create new knowledge base
   ↓
Step 10: Rebuild vector database
   ↓
✅ Chatbot now has updated stored data!
```

---

## 📋 Detailed File-by-File Guide

### 🟢 **step1_setup_test.py** - KEEP (Optional)
**Purpose**: Test Python environment  
**When to use**: First time setup  
**Keep it?**: Yes, useful for troubleshooting  
**Action**: Keep as-is

```bash
# Use when:
python scripts/step1_setup_test.py
# To verify Python version, packages, etc.
```

---

### 🟢 **step2_test_gemini.py** - KEEP (Optional)
**Purpose**: Test Google Gemini API connection  
**When to use**: Verify API key works  
**Keep it?**: Yes, useful for testing  
**Action**: Keep as-is

```bash
# Use when:
python scripts/step2_test_gemini.py
# To test if GOOGLE_API_KEY works
```

---

### 🟢 **step3_download_data.py** - KEEP (Important)
**Purpose**: Download latest data from UN and World Bank  
**When to use**: Quarterly, to update stored data  
**Keep it?**: YES - Important for updates  
**Action**: Keep as-is

```bash
# Use when:
python scripts/step3_download_data.py
# When UN releases new quarterly data
# When you want to refresh stored data
```

**Note**: This downloads the **historical data** that gets stored in ChromaDB. The chatbot will still fetch **live data** separately!

---

### 🟡 **step4_verify_data.py** - KEEP (Optional)
**Purpose**: Verify downloaded data is valid  
**When to use**: After downloading new data  
**Keep it?**: Yes, useful for validation  
**Action**: Keep as-is

---

### 🟡 **step4b_convert_excel_to_csv.py** - KEEP (Optional)
**Purpose**: Convert Excel files to CSV  
**When to use**: If you have Excel data files  
**Keep it?**: Yes, utility tool  
**Action**: Keep as-is

---

### 🟢 **step5_clean_data.py** - KEEP (Important)
**Purpose**: Clean and format downloaded data  
**When to use**: After downloading new data  
**Keep it?**: YES - Important for data pipeline  
**Action**: Keep as-is

```bash
# Use when:
python scripts/step5_clean_data.py
# After step3 (downloading data)
# Before step6 (creating knowledge base)
```

---

### 🟢 **step6_create_knowledge_base.py** - KEEP (Important)
**Purpose**: Convert cleaned data into JSONL documents  
**When to use**: After cleaning data  
**Keep it?**: YES - Core data pipeline  
**Action**: Keep as-is

```bash
# Use when:
python scripts/step6_create_knowledge_base.py
# After step5 (cleaning data)
# Creates documents for vector database
```

---

### 🟢 **step7_build_vector_db.py** - KEEP (Critical)
**Purpose**: Build ChromaDB vector database  
**When to use**: Initial setup or after updating knowledge base  
**Keep it?**: YES - Essential  
**Action**: Keep as-is

```bash
# Use when:
python scripts/step7_build_vector_db.py
# First time setup (creates ChromaDB)
# After updating knowledge base
```

**This is what creates the 11,346 documents in ChromaDB!**

---

### 🔴 **step8_build_chatbot.py** - DELETE (Obsolete)
**Purpose**: Old chatbot building script  
**When to use**: NEVER (replaced by unified system)  
**Keep it?**: NO - No longer needed  
**Action**: DELETE

**Why delete?**  
- You now use `app.py` and `telegram_bot.py` directly
- This script built the old system
- No longer compatible with unified system

---

### 🔴 **step9_process_ess_reports.py** - NOT NEEDED (ESS is Live-Only)
**Purpose**: Process ESS PDF reports (if you had any downloaded)  
**When to use**: NEVER (ESS data is fetched live from website)  
**Keep it?**: Optional (only if you want to add downloaded ESS PDFs in future)  
**Action**: Keep but don't use

**Why not needed?**
- ESS data is fetched **live** from website every query
- No need to download or process PDFs
- System scrapes ESS website directly
- Auto-updates automatically!

```bash
# You DON'T need to run this
# ESS data is fetched live automatically
```

**If you ever want to add downloaded ESS PDFs:**
1. Put PDFs in `data/raw/ess/`
2. Run: `python scripts/step9_process_ess_reports.py`
3. Run: `python scripts/step10_rebuild_vector_db.py`

**But for now:** ESS is 100% live, no downloads needed! ✅

---

### 🟢 **step10_rebuild_vector_db.py** - KEEP (Important)
**Purpose**: Rebuild vector database with new data  
**When to use**: After adding new documents  
**Keep it?**: YES - For updates  
**Action**: Keep as-is

```bash
# Use when:
python scripts/step10_rebuild_vector_db.py
# After step9 (processing ESS reports)
# After updating knowledge base
# When you want to refresh ChromaDB
```

---

### 🔴 **fix_logo.py** - DELETE (Utility)
**Purpose**: One-time logo fixing script  
**When to use**: Never (one-time fix)  
**Keep it?**: NO - No longer needed  
**Action**: DELETE

---

## 🎯 Summary Table

| Script | Status | Purpose | Keep? |
|--------|--------|---------|-------|
| step1_setup_test.py | Optional | Test environment | ✅ |
| step2_test_gemini.py | Optional | Test API | ✅ |
| step3_download_data.py | Important | Download data | ✅ |
| step4_verify_data.py | Optional | Verify data | ✅ |
| step4b_convert_excel_to_csv.py | Optional | Convert files | ✅ |
| step5_clean_data.py | Important | Clean data | ✅ |
| step6_create_knowledge_base.py | Important | Create docs | ✅ |
| step7_build_vector_db.py | Critical | Build ChromaDB | ✅ |
| step8_build_chatbot.py | Obsolete | Old system | ❌ DELETE |
| step9_process_ess_reports.py | Optional | Process ESS PDFs | ⚠️ (not needed - ESS is live) |
| step10_rebuild_vector_db.py | Important | Rebuild DB | ✅ |
| fix_logo.py | Utility | One-time fix | ❌ DELETE |

---

## 🔄 When to Run Each Script

### Initial Setup (Done Once):
```bash
1. python scripts/step1_setup_test.py       # Optional: test setup
2. python scripts/step2_test_gemini.py      # Optional: test API
3. python scripts/step3_download_data.py    # Download UN/World Bank data
4. python scripts/step5_clean_data.py       # Clean downloaded data
5. python scripts/step6_create_knowledge_base.py  # Create documents
6. python scripts/step7_build_vector_db.py  # Build ChromaDB
✅ Done! Now run: streamlit run app.py
```

### Quarterly Update (When UN Releases New Data):
```bash
1. python scripts/step3_download_data.py    # Download new data
2. python scripts/step5_clean_data.py       # Clean new data
3. python scripts/step6_create_knowledge_base.py  # Update knowledge base
4. python scripts/step10_rebuild_vector_db.py  # Rebuild ChromaDB
✅ Updated! Chatbot now has latest stored data
```

### Adding New ESS Reports:
```bash
# NOTE: Not needed! ESS data is fetched live automatically
# But if you want to add downloaded ESS PDFs:
1. Download ESS PDF reports manually to data/raw/ess/
2. python scripts/step9_process_ess_reports.py  # Process PDFs
3. python scripts/step10_rebuild_vector_db.py   # Rebuild ChromaDB
✅ Updated! But live ESS fetching continues automatically
```

### Never Run:
- ❌ step8_build_chatbot.py (obsolete)
- ❌ fix_logo.py (one-time utility)

---

## 💡 Understanding the Two Data Systems

### System 1: Stored/Downloaded Data (ChromaDB)
- **Updated by**: Running step3 → step5 → step6 → step7
- **Frequency**: Quarterly (when UN releases data) or manually
- **Used by**: ALL queries (always searched first)
- **Contains**: 11,346 historical documents (1995-2026)

### System 2: Live Data (API + Web Scraping)
- **Updated by**: Automatic! No scripts needed
- **Frequency**: Real-time, every query
- **Used by**: When "Fetch Live Data" is enabled (default: ON)
- **Fetches**:
  - World Bank API (latest indicators)
  - ESS Website (current publications)

### How They Work Together:
```
User Question → Search ChromaDB (System 1)
             ↓
          Fetch Live Data (System 2)
             ↓
          Combine Both
             ↓
          Generate Answer
```

**You get the best of both worlds!**
- Historical data from ChromaDB (comprehensive)
- Latest data from live sources (current)

---

## 🗑️ Action Items for You

### Delete These 2 Files:
```bash
del scripts\step8_build_chatbot.py
del scripts\fix_logo.py
```

### Keep All Others
All other scripts are useful for maintaining and updating your data!

---

## ❓ Common Questions

### Q: Do I need to run these scripts regularly?
**A**: No! Only when you want to **update the stored data** in ChromaDB. The live fetching happens automatically.

### Q: What if I never run the update scripts?
**A**: Your chatbot will still work! It will use:
- Existing stored data in ChromaDB (11,346 docs)
- PLUS live data from World Bank API and ESS website

### Q: How often should I update the stored data?
**A**: 
- **UN data**: Quarterly (when they release new data)
- **ESS reports**: When new PDFs are published (check their website)
- **Or never**: If current data is sufficient for your needs

### Q: Can the chatbot work without the stored data?
**A**: Technically yes, with live data only, but you'd lose the comprehensive historical coverage. The stored data is essential for good answers!

---

## 📝 Recommendation

**Delete**: `step8_build_chatbot.py` and `fix_logo.py`  
**Keep**: All other step files (they're useful for data maintenance)

The stored data (ChromaDB) is **essential** and complements the live data perfectly!

---

**Next Step**: Delete the 2 obsolete files, then test your system:
```bash
python test_unified_system.py
streamlit run app.py
```
