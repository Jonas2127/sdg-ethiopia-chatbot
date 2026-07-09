# Troubleshooting Guide

## Common Issues and Solutions

### ❌ Error: "DAILY QUOTA EXCEEDED" or "429 RESOURCE_EXHAUSTED"

**What it means:**  
You've used 1,500+ Gemini API requests today (quota is per Google account, not per API key).

**Solutions (in order of recommendation):**

1. **✅ BEST: Switch to `app.py`**
   ```bash
   python -m streamlit run app.py
   ```
   - Uses fewer API calls (1 per question vs 2-4 in hybrid)
   - Fast and reliable
   - No rate limits

2. **⏰ Wait for quota reset**
   - Quota resets at **10:00 AM Ethiopia time** (midnight Pacific Time)
   - Check at: https://aistudio.google.com/apikey → "View API usage"

3. **🔑 Use different Google account**
   - Go to: https://aistudio.google.com/apikey
   - **Sign OUT of current Google account**
   - **Sign IN with different account**
   - Create new API key
   - Update `.env` file:
     ```
     GOOGLE_API_KEY=your_new_key_here
     ```
   - **Why changing key alone doesn't work:** Quota is tied to your Google account, not the key

---

### ❌ Error: "Streamlit is not recognized"

**Problem:**  
`streamlit` command not in Windows PATH.

**Solution:**  
Use `python -m streamlit` instead:
```bash
python -m streamlit run app.py
```

---

### ❌ "Live Data Points: 0" in `app_hybrid.py`

**Problem:**  
Your question didn't contain keywords that trigger live data fetch.

**Keywords that work:**
- poverty, poor, income
- education, school, enrollment, literacy, student
- health, mortality, infant, child, death
- electricity, power, energy
- water, sanitation
- forest, trees
- gdp, economy, growth

**Examples:**
- ❌ "Tell me about Ethiopia" → No keywords
- ✅ "What is Ethiopia's poverty rate?" → Contains "poverty"
- ✅ "Show me education statistics" → Contains "education"

**Also check:**
- Is "Fetch Live Data" checkbox enabled in sidebar?

---

### ❌ Countdown loops repeatedly (never answers)

**Problem:**  
Daily quota is already exhausted. Waiting 60 seconds won't help.

**Why it happens:**
- After countdown, API is called again
- API still returns 429 (quota exhausted)
- System counts down again
- Infinite loop

**Solution:**
1. **Stop the app** (Ctrl+C in terminal)
2. **Use `app.py` instead**:
   ```bash
   python -m streamlit run app.py
   ```
3. Or wait until tomorrow 10 AM

---

### ❌ "No module named 'streamlit'" or other imports

**Problem:**  
Dependencies not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

If still fails on Windows:
```bash
pip install pandas numpy streamlit sentence-transformers chromadb google-generativeai python-dotenv requests python-telegram-bot
```

---

### ❌ Logo not showing or blurred

**Problem:**  
Logo file missing or wrong path.

**Check:**
1. Does `assets/ess_logo_fixed.png` exist?
2. If not, run:
   ```bash
   python scripts/fix_logo.py
   ```

**Manual fix:**
- Use any circular logo image (400x400px, transparent background)
- Save as `assets/ess_logo_fixed.png`

---

### ❌ "Can't open file 'streamlit'"

**Problem:**  
Using `python streamlit run app.py` (wrong syntax).

**Solution:**  
Use `python -m streamlit run app.py` (note the `-m` flag):
```bash
python -m streamlit run app.py
```

---

### ❌ ChromaDB error: "Collection not found"

**Problem:**  
Vector database not created yet.

**Solution:**  
Run the setup scripts in order:
```bash
python scripts/step6_create_knowledge_base.py
python scripts/step7_build_vector_db.py
```

---

### ❌ Telegram bot: "TELEGRAM_BOT_TOKEN not found"

**Problem:**  
Token not set in `.env` file.

**Solution:**
1. Get token from @BotFather on Telegram:
   - Send `/newbot` to @BotFather
   - Choose name and username
   - Copy the token

2. Add to `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

3. Run bot:
   ```bash
   python telegram_bot.py
   ```

---

## Quick Diagnostic Commands

### Check if Python is working
```bash
python --version
```
Should show: `Python 3.11` or higher

### Check if packages are installed
```bash
pip list | findstr streamlit
pip list | findstr chromadb
```

### Check if vector DB exists
```bash
dir chroma_db
```
Should show files inside

### Test Gemini API key
```bash
python scripts/step2_test_gemini.py
```

### Check API quota usage
Visit: https://aistudio.google.com/apikey  
Click on your key → "View API usage"

---

## Rate Limit Details

### Gemini API Free Tier Limits
- **Per minute:** 15 requests
- **Per day:** 1,500 requests
- **Quota resets:** Midnight Pacific Time = 10 AM Ethiopia time

### API Calls per Question
- **app.py:** 1 call (Gemini only)
- **app_hybrid.py:** 2-4 calls (Gemini + World Bank API)
- **telegram_bot.py:** 1 call (Gemini only)

### How to avoid hitting limits
✅ Use `app.py` for daily work  
✅ Use `app_hybrid.py` sparingly (< 50 questions/day)  
✅ Don't spam refresh or ask same question repeatedly  
✅ For heavy testing, use different Google account  

---

## Still Having Issues?

### Check these files for detailed info:
- `docs/PROJECT_EXPLANATION.md` - How the system works
- `docs/SAMPLE_QUESTIONS_COMPARISON.md` - Which questions work where
- `docs/REAL_TIME_DATA_GUIDE.md` - How live data works
- `docs/DEPLOY_TELEGRAM_BOT.md` - Telegram setup

### Test the system step by step:
```bash
# 1. Test API key
python scripts/step2_test_gemini.py

# 2. Test vector DB
python scripts/step8_build_chatbot.py

# 3. Test web app
python -m streamlit run app.py
```

---

## Emergency Fix: Start Fresh

If everything is broken, reset the system:

```bash
# 1. Check your API key is valid
#    Visit: https://aistudio.google.com/apikey

# 2. Recreate knowledge base
python scripts/step6_create_knowledge_base.py
python scripts/step7_build_vector_db.py

# 3. Test chatbot
python scripts/step8_build_chatbot.py

# 4. Run app
python -m streamlit run app.py
```

---

## Contact for Help

**Student Developer:** [Your Name]  
**Institution:** Bahir Dar University  
**Supervisor:** Ethiopian Statistical Service  

**Useful Links:**
- Gemini API: https://aistudio.google.com/apikey
- Streamlit Docs: https://docs.streamlit.io/
- World Bank API: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
