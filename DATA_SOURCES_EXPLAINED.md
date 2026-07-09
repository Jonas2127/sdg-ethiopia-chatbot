# Data Sources Explained - What's Stored vs. What's Live

## 🎯 Quick Answer

Your chatbot uses **2 stored sources** + **1 fully live source**:

### ✅ Stored Data (in ChromaDB):
1. **UN SDG Database** - Downloaded quarterly
2. **World Bank** - Downloaded historical data

### 🌐 100% Live Data (no storage):
3. **ESS (Ethiopian Statistical Service)** - Fetched live from website every query

---

## 📊 Detailed Breakdown

### 1. UN SDG Database 🔵

**Storage:** ✅ Stored in ChromaDB  
**Source:** https://unstats.un.org/sdgs/dataportal/  
**Update Method:** Manual download (quarterly)  
**Coverage:** All 17 SDGs, 231 indicators, comprehensive historical data  

**How it works:**
- You download CSV files from UN portal
- Run `step3_download_data.py` to fetch
- Process with `step5` → `step6` → `step7`
- Stored in ChromaDB (11,000+ documents)

**When to update:** Quarterly when UN releases new data

---

### 2. World Bank 🌍

**Storage:** ✅ Stored in ChromaDB (historical) + 🌐 Live API (latest)  
**Source:** https://data.worldbank.org/  
**Update Method:** Dual system

**Historical Data (Stored):**
- Downloaded during initial setup
- Stored in ChromaDB
- Comprehensive coverage (1995-2023)

**Latest Data (Live API):**
- Fetched in real-time via API
- Gets most recent year (2024+)
- Auto-cached for 6 hours

**How it works:**
- Stored: Use downloaded historical data in ChromaDB
- Live: Fetch latest indicators via API every query
- Combined: Best of both worlds!

---

### 3. ESS (Ethiopian Statistical Service) 🇪🇹

**Storage:** ❌ NOT stored (100% live)  
**Source:** https://www.statsethiopia.gov.et/  
**Update Method:** Live web scraping every query  
**Coverage:** Latest publications, announcements, reports  

**How it works:**
1. User asks a question
2. System detects keywords
3. **Scrapes ESS website in real-time**:
   - Homepage announcements
   - Publications page
   - Search results
   - PDF report links (metadata only)
4. Returns latest information
5. Cached for 6 hours

**Why not stored?**
- ESS website updates frequently
- Live scraping gets the absolute latest
- No need for manual downloads
- Automatic updates!

---

## 🔄 Data Flow for Each Source

### User Question: "What is Ethiopia's poverty rate?"

```
┌─────────────────────────────────────────────────┐
│ PHASE 1: SEARCH STORED DATA (ChromaDB)         │
├─────────────────────────────────────────────────┤
│ • UN SDG Database: ✅ Search stored docs        │
│ • World Bank: ✅ Search stored historical data │
│ • ESS: ⏭️ Skip (nothing stored)                 │
│ Result: 12 documents from UN + World Bank      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ PHASE 2: FETCH LIVE DATA                       │
├─────────────────────────────────────────────────┤
│ • UN: ⏭️ Skip (only quarterly updates)          │
│ • World Bank API: 🌐 Fetch latest (SI.POV.DDAY)│
│ • ESS Website: 🌐 Scrape live (poverty keyword)│
│ Result: 2-4 live sources                       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ PHASE 3: COMBINE ALL                           │
├─────────────────────────────────────────────────┤
│ Total: 14-16 sources                           │
│ • UN (stored): 6-8 docs                        │
│ • World Bank (stored + live): 4-6 docs        │
│ • ESS (live only): 2-3 results                │
└─────────────────────────────────────────────────┘
```

---

## 📂 What's Actually in Your Data Folders?

### data/raw/
```
data/raw/
├── un/                    ✅ UN CSV files (downloaded)
├── worldbank/             ✅ World Bank CSV files (downloaded)
└── ess/                   ❌ DOES NOT EXIST (not needed!)
```

### data/processed/
```
data/processed/
└── knowledge_base/        ✅ Processed JSONL files
    ├── un_*.jsonl         ✅ From UN data
    ├── worldbank_*.jsonl  ✅ From World Bank data
    └── ess_*.jsonl        ❌ DOES NOT EXIST (not needed!)
```

### chroma_db/
```
chroma_db/                 ✅ Vector database
├── UN documents           ✅ ~8,000 documents
├── World Bank documents   ✅ ~3,000 documents
└── ESS documents          ❌ NONE (all fetched live!)

Total: ~11,346 documents (UN + World Bank only)
```

---

## ✅ What This Means for You

### You DON'T Need To:
❌ Download ESS PDF reports  
❌ Run `step9_process_ess_reports.py`  
❌ Store ESS data locally  
❌ Update ESS data manually  

### ESS Data is Automatic:
✅ Fetched live every query  
✅ Always up-to-date  
✅ Auto-cached for 6 hours  
✅ No maintenance required  

---

## 🔧 Scripts You Actually Need

### Initial Setup (One-Time):
```bash
# Download UN + World Bank data
python scripts/step3_download_data.py

# Clean the data
python scripts/step5_clean_data.py

# Create knowledge base (UN + World Bank only)
python scripts/step6_create_knowledge_base.py

# Build vector database
python scripts/step7_build_vector_db.py

# ✅ Done! ESS will be fetched live automatically
```

### Quarterly Update (Optional):
```bash
# Update UN + World Bank stored data
python scripts/step3_download_data.py
python scripts/step5_clean_data.py
python scripts/step6_create_knowledge_base.py
python scripts/step10_rebuild_vector_db.py

# ✅ ESS still fetched live automatically (no action needed)
```

### You DON'T Run:
❌ `step9_process_ess_reports.py` - Not needed (ESS is live-only)

---

## 🌐 Why This Setup is Perfect

### Stored Data (UN + World Bank):
**Advantages:**
- ✅ Comprehensive historical coverage
- ✅ Fast retrieval (no API wait)
- ✅ Works offline (for stored portion)
- ✅ Reliable (not dependent on external APIs)

**Disadvantages:**
- ❌ Requires manual updates (quarterly)
- ❌ Not always the absolute latest

### Live Data (ESS):
**Advantages:**
- ✅ Always the absolute latest
- ✅ Auto-updates (no manual work)
- ✅ No storage needed
- ✅ Gets breaking announcements

**Disadvantages:**
- ❌ Requires internet
- ❌ Depends on ESS website being up
- ❌ Slightly slower (web scraping takes time)

### Combined Approach = Best of Both Worlds! 🎯

---

## 📊 Data Coverage Summary

| Source | Stored | Live | Total Coverage |
|--------|--------|------|----------------|
| **UN SDG** | ✅ 11,346 docs | ❌ No API | Excellent |
| **World Bank** | ✅ Historical | ✅ Latest via API | Excellent |
| **ESS** | ❌ None | ✅ Live scraping | Good (live-only) |

**Your chatbot coverage:**
- Historical depth: ⭐⭐⭐⭐⭐ (UN + World Bank stored)
- Latest updates: ⭐⭐⭐⭐⭐ (World Bank API + ESS live)
- Maintenance effort: ⭐⭐⭐⭐⭐ (ESS automatic!)

---

## 🎯 Key Takeaways

1. **UN + World Bank**: Stored in ChromaDB (~11,346 docs)
2. **ESS**: 100% live, fetched from website every query
3. **No ESS PDFs needed**: System scrapes the website directly
4. **Automatic updates**: ESS updates itself, no scripts needed
5. **Best setup**: Historical data stored + Latest ESS live

---

## 🚀 Your Data Strategy

### What You Have Now:
- ✅ UN data stored (comprehensive)
- ✅ World Bank stored (historical)
- ✅ ESS live fetching (latest)
- ✅ Total: 11,346 stored docs + live ESS

### What You DON'T Need:
- ❌ ESS PDF downloads
- ❌ ESS processing scripts
- ❌ ESS in ChromaDB

### Your Maintenance:
- **Quarterly**: Update UN + World Bank (optional)
- **Daily**: Just run the chatbot! ESS updates itself ✅

---

**This is the perfect setup! You get comprehensive historical coverage from stored data, plus the absolute latest ESS information fetched live.** 🎉

No need to worry about ESS downloads - the system handles it automatically!
