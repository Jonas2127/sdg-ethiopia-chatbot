# Sample Questions: app.py vs app_hybrid.py

## 🎯 Quick Answer: Which App Should I Use?

### ✅ Use `app.py` for:
- Daily work and testing
- Demo to your supervisor
- When you need fast, reliable answers
- Heavy usage (100+ questions)

### 🌐 Use `app_hybrid.py` for:
- Showing off "real-time capability"
- Light usage only (< 50 questions/day)
- When you specifically need latest World Bank data

---

## Understanding the Difference

### `app.py` (Stored Data Only)
- Uses **11,346 historical records** from the database
- **No API calls** to external sources
- **Fast and reliable** - no rate limits
- Data from **1995-2026** (UN SDG Database + World Bank historical)
- **RECOMMENDED for daily use and demos**

### `app_hybrid.py` (Stored + Live Data)
- Uses **stored database** (11,346 records)
- **+ Live API calls** to World Bank (real-time data)
- **Can hit rate limits** (1,500 requests/day)
- Shows "[LIVE DATA]" tag in responses
- **Use to showcase "real-time capability"** but not for heavy use

---

## Sample Questions Comparison

### ✅ Questions BOTH Can Answer

Both `app.py` and `app_hybrid.py` can answer these equally well:

1. **"What is Ethiopia's poverty rate?"**
   - Both: Show historical poverty data from database (1995-2015)

2. **"How many schools have computers in Ethiopia?"**
   - Both: Show education technology indicators (2020-2022)

3. **"What is the child mortality rate in Ethiopia?"**
   - Both: Show historical mortality data

4. **"What percentage of population has access to water?"**
   - Both: Show water access statistics

---

### 🌐 Questions Where `app_hybrid.py` Shows Live Data

These questions trigger **live API fetches** in `app_hybrid.py`:

#### Example 1: Poverty (Recent)
**Question:** *"What is Ethiopia's latest poverty rate?"*

- **app.py**: Shows 2015 data (37.4%, 24.9%, 29.1% from different sources)
- **app_hybrid.py**: Shows 2015 data + **[LIVE DATA]** with most recent World Bank update (if available)

#### Example 2: Education (Current)
**Question:** *"What is Ethiopia's current primary school enrollment?"*

- **app.py**: Shows 2020-2022 school computer/internet access data
- **app_hybrid.py**: Shows stored data + **[LIVE DATA]** primary enrollment rate from World Bank API (e.g., 85.3% in 2024)

#### Example 3: Electricity (Latest)
**Question:** *"Show me the latest electricity access in Ethiopia"*

- **app.py**: Shows 2020-2022 electricity access from database
- **app_hybrid.py**: Shows stored data + **[LIVE DATA]** with most recent World Bank figure

#### Example 4: Health (Real-time)
**Question:** *"What are Ethiopia's most recent health statistics?"*

- **app.py**: Shows historical health indicators (mortality, life expectancy)
- **app_hybrid.py**: Shows stored data + **[LIVE DATA]** with latest health metrics from World Bank

#### Example 5: Economy (Current)
**Question:** *"What is Ethiopia's current GDP growth rate?"*

- **app.py**: Shows historical economic data from database
- **app_hybrid.py**: Shows stored data + **[LIVE DATA]** with latest GDP growth from World Bank

---

## How to See the Difference

### In `app_hybrid.py`, look for these indicators:

1. **Top of answer**: Shows "[LIVE DATA]" tag if real-time data was fetched

2. **Metrics section**: 
   - **Stored Documents**: 15 (from database)
   - **Live Data Points**: 1-2 (from API)

3. **Sources section**: Expands to show:
   - 🌐 **Live Data** (Fetched Just Now) - with timestamps
   - 📊 **Stored Database** - historical records

---

## Keywords That Trigger Live Data

The hybrid app fetches live data when your question contains these words:

- **Poverty**: poverty, poor, income
- **Education**: education, school, enrollment, literacy, learning, student
- **Health**: health, mortality, infant, child, death, life expectancy
- **Infrastructure**: electricity, power, energy, water, sanitation, toilet
- **Environment**: forest, trees, deforestation
- **Economy**: gdp, economy, economic, growth

---

## When to Use Which App

### Use `app.py` when:
✅ You want **fast, reliable** answers  
✅ You're **demoing to your supervisor**  
✅ You don't need "latest" data  
✅ You want to **avoid rate limits**  
✅ You're doing **heavy testing** (many questions)

**Command:**
```bash
python -m streamlit run app.py
```

---

### Use `app_hybrid.py` when:
✅ You want to **showcase real-time capability**  
✅ You need **"latest available" data**  
✅ You're doing **light testing** (< 50 questions/day)  
✅ You want to **impress with [LIVE DATA] tag**

**Command:**
```bash
python -m streamlit run app_hybrid.py
```

---

## Example Demo Script

When presenting to your supervisor at Ethiopian Statistical Service:

### Part 1: Show Regular App (5 minutes)
```bash
python -m streamlit run app.py
```

**Say:**  
*"This is our main chatbot with 11,346 historical records from UN SDG Database and World Bank."*

**Ask sample questions:**
1. "What is Ethiopia's poverty rate?"
2. "How many schools have computers?"
3. "What is the child mortality rate?"

### Part 2: Show Hybrid App (2 minutes)
```bash
python -m streamlit run app_hybrid.py
```

**Say:**  
*"This version can also fetch real-time data from World Bank API when needed."*

**Ask:**
1. "What is Ethiopia's latest poverty rate?"  
   → Point to **[LIVE DATA]** tag and timestamp

**Say:**  
*"However, for daily use we recommend the regular version because it's faster and more reliable."*

---

## Troubleshooting

### If `app_hybrid.py` shows "Live Data Points: 0"
**Reason**: Your question didn't contain any trigger keywords

**Solution**: Add words like "latest", "current", "poverty", "education", etc.

**Example:**
- ❌ "Tell me about statistical data" → No keywords = 0 live data
- ✅ "What is the latest poverty rate?" → Contains "poverty" = fetches live data

---

### If you get "DAILY QUOTA EXCEEDED"
**Reason**: You've used 1,500+ API requests today (quota tied to Google account)

**Solutions:**
1. **Switch to app.py** immediately (no API calls)
2. **Wait until 10 AM Ethiopia time** (quota resets)
3. **Use different Google account** for new API key (go to https://aistudio.google.com/apikey)

---

## Summary Table

| Feature | app.py | app_hybrid.py |
|---------|---------|---------------|
| **Speed** | Fast (3-4 sec) | Slower (5-7 sec) |
| **Data Source** | Stored only | Stored + Live API |
| **Rate Limits** | None | 1,500/day |
| **Best For** | Daily use, demos | Showcasing capability |
| **Reliability** | Very high | Medium (API dependency) |
| **API Calls/Question** | 1 (Gemini only) | 2-4 (Gemini + World Bank) |

---

## Recommendation

✅ **For your internship presentation**: Use `app.py` as the main demo, briefly show `app_hybrid.py` as a "bonus feature" to demonstrate technical capability.

✅ **For daily use**: Stick with `app.py`

✅ **For impressing tech-savvy people**: Show `app_hybrid.py` with [LIVE DATA] tags
