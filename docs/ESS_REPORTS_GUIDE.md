# Adding ESS Reports to Your Chatbot

## Overview

Your chatbot currently uses:
- ✅ **UN SDG Database** (11,316 records)
- ✅ **World Bank API** (30 historical + live data)

You can add:
- 📄 **ESS Weekly Reports**
- 📄 **ESS Monthly Bulletins**
- 📄 **ESS Quarterly Reports**
- 📄 **ESS Annual Statistics**

---

## Step-by-Step Guide

### Step 1: Install Required Packages

```bash
pip install PyPDF2 python-docx
```

These packages allow reading PDF and Word documents.

---

### Step 2: Prepare Your ESS Reports

1. **Create folder** for ESS reports:
   ```bash
   cd C:\Users\HP\.vscode\Documents\ESSproject 2\sdg-ethiopia-chatbot
   mkdir data\raw\ess_reports
   ```

2. **Copy your ESS reports** into this folder

**Supported formats:**
- ✅ PDF (.pdf) - Weekly/Monthly/Quarterly/Annual reports
- ✅ Excel (.xlsx, .xls) - Statistical tables
- ✅ Word (.docx, .doc) - Narrative reports
- ✅ CSV (.csv) - Data tables

**Example file structure:**
```
data/raw/ess_reports/
├── ESS_Weekly_Report_Week1_2026.pdf
├── ESS_Monthly_Bulletin_June_2026.pdf
├── ESS_Quarterly_Report_Q2_2026.docx
├── ESS_Annual_Statistics_2025.xlsx
├── poverty_data_monthly.csv
└── education_statistics_2026.xlsx
```

---

### Step 3: Process ESS Reports

```bash
python scripts/step9_process_ess_reports.py
```

**What this does:**
- Reads all files from `data/raw/ess_reports/`
- Extracts text from PDFs, Word docs
- Extracts data from Excel, CSV
- Splits long documents into chunks (1000 chars each)
- Saves to `data/processed/ess_documents.jsonl`

**Output example:**
```
============================================================
PROCESSING ESS REPORTS
============================================================

Found 5 files
------------------------------------------------------------

Processing: ESS_Weekly_Report_Week1_2026.pdf
  ✓ Extracted 8543 characters
  ✓ Split into 9 chunks
  ✓ Type: Weekly Report

Processing: ESS_Monthly_Bulletin_June_2026.pdf
  ✓ Extracted 15234 characters
  ✓ Split into 16 chunks
  ✓ Type: Monthly Report

...

✓ PROCESSED 5 FILES
✓ CREATED 67 DOCUMENT CHUNKS
============================================================
```

---

### Step 4: Rebuild Vector Database

```bash
python scripts/step10_rebuild_vector_db.py
```

**What this does:**
- Loads original 11,346 documents (UN + World Bank)
- Loads new ESS documents
- Combines them together
- Rebuilds the vector database with ALL documents
- Generates embeddings for new ESS reports

**Output example:**
```
============================================================
REBUILDING VECTOR DATABASE WITH ESS REPORTS
============================================================

[1/5] Loading embedding model...
✓ Model loaded

[2/5] Connecting to database...
✓ Deleted old collection
✓ Created new collection

[3/5] Loading original knowledge base...
✓ Loaded 11,346 original documents

[4/5] Loading ESS reports...
✓ Loaded 67 ESS document chunks

✓ Total documents: 11,413
  - Original (UN/World Bank): 11,346
  - ESS Reports: 67

[5/5] Building vector database...
  Processed batch 1/115 (100 docs)
  Processed batch 2/115 (100 docs)
  ...
  Processed batch 115/115 (13 docs)

✓ VECTOR DATABASE REBUILT SUCCESSFULLY
============================================================
Total documents: 11,413
  - UN/World Bank: 11,346
  - ESS Reports: 67
============================================================
```

---

### Step 5: Run Your Chatbot

```bash
python -m streamlit run app.py
```

**Your chatbot now answers questions about:**
- ✅ UN SDG data (1995-2026)
- ✅ World Bank data
- ✅ **ESS Weekly Reports**
- ✅ **ESS Monthly Bulletins**
- ✅ **ESS Quarterly Reports**
- ✅ **ESS Annual Statistics**

---

## Example Questions After Adding ESS Reports

### Before (UN + World Bank only):
**Q:** *"What is the latest poverty data from ESS?"*  
**A:** "I don't have ESS-specific data. Here's World Bank data..."

### After (With ESS Reports):
**Q:** *"What is the latest poverty data from ESS?"*  
**A:** "According to the ESS Monthly Bulletin (June 2026), poverty rate in Ethiopia is 27.3%... [FULL DETAILS FROM ESS REPORT]"

### New Questions You Can Ask:
1. *"What does the ESS weekly report say about inflation?"*
2. *"Show me ESS quarterly statistics on employment"*
3. *"What are the key findings in the ESS annual report?"*
4. *"Compare UN data with ESS monthly bulletin on education"*

---

## File Naming Recommendations

To help the chatbot identify report types, name your files clearly:

### ✅ Good Names:
- `ESS_Weekly_Report_Week12_2026.pdf`
- `ESS_Monthly_Bulletin_July_2026.pdf`
- `ESS_Quarterly_Q3_2026.docx`
- `ESS_Annual_Statistics_2025.xlsx`
- `poverty_monthly_data_June_2026.csv`

### ❌ Avoid:
- `report.pdf` (too generic)
- `doc1.docx` (unclear)
- `data.xlsx` (unclear)

**Keywords detected:**
- **Weekly:** weekly, week
- **Monthly:** monthly, month
- **Quarterly:** quarterly, quarter, Q1, Q2, Q3, Q4
- **Annual:** annual, yearly, year

---

## Updating with New Reports

When you get new ESS reports:

```bash
# 1. Add new files to folder
copy new_report.pdf data\raw\ess_reports\

# 2. Process new reports
python scripts/step9_process_ess_reports.py

# 3. Rebuild database
python scripts/step10_rebuild_vector_db.py

# 4. Run chatbot
python -m streamlit run app.py
```

---

## Technical Details

### Document Chunking
- Long reports are split into 1000-character chunks
- Each chunk is embedded separately
- Chatbot retrieves most relevant chunks (not full reports)
- This allows handling large ESS reports efficiently

### Metadata Stored
For each ESS document:
```json
{
  "source": "ESS",
  "filename": "ESS_Monthly_Bulletin_June_2026.pdf",
  "file_type": "PDF Report",
  "report_type": "Monthly Report",
  "chunk": "3/16",
  "processed_at": "2026-07-07 14:30:22"
}
```

### Search Priority
When user asks a question:
1. Chatbot searches ALL documents (UN + World Bank + ESS)
2. Returns top 20 most relevant chunks
3. May include mix of UN data + ESS reports
4. Gemini AI synthesizes answer from all sources

---

## Troubleshooting

### ❌ "PyPDF2 not installed"
```bash
pip install PyPDF2
```

### ❌ "python-docx not installed"
```bash
pip install python-docx
```

### ❌ "No files found in ess_reports"
- Check folder exists: `data/raw/ess_reports/`
- Add your ESS reports to this folder
- Run step 9 again

### ❌ "Original knowledge base not found"
- Run: `python scripts/step6_create_knowledge_base.py`
- Run: `python scripts/step7_build_vector_db.py`
- Then run steps 9 and 10

### ❌ PDF extraction failed
- Some PDFs have image-based text (scanned documents)
- For scanned PDFs, you need OCR (Optical Character Recognition)
- Try converting PDF to text first, or use typed (not scanned) PDFs

---

## Advanced: Adding OCR for Scanned PDFs

If your ESS reports are scanned images, install OCR:

```bash
pip install pytesseract Pillow pdf2image
```

Then modify `step9_process_ess_reports.py` to use OCR (requires Tesseract installation on Windows).

---

## Summary

### Before:
- 11,346 documents (UN + World Bank)

### After Adding ESS Reports:
- 11,346 + [your ESS documents]
- Chatbot knows about ESS weekly/monthly/quarterly/annual reports
- Can answer ESS-specific questions
- Can compare UN/World Bank with ESS data

### Commands:
```bash
# 1. Install packages
pip install PyPDF2 python-docx

# 2. Add reports to data/raw/ess_reports/

# 3. Process reports
python scripts/step9_process_ess_reports.py

# 4. Rebuild database
python scripts/step10_rebuild_vector_db.py

# 5. Run chatbot
python -m streamlit run app.py
```

---

## Benefits for Your Internship

✅ **More comprehensive** - ESS + UN + World Bank data  
✅ **More relevant** - Local Ethiopian data from ESS  
✅ **More current** - Latest ESS reports  
✅ **More valuable** - Unique to Ethiopian Statistical Service  
✅ **Impressive demo** - Show how chatbot handles multiple data sources  

This makes your chatbot a real tool for ESS staff, not just a demo project!
