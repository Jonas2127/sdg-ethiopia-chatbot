# Data Sources Documentation

## Primary Data Sources for Ethiopia SDG Data

### 1. UN SDG Database
**URL:** https://unstats.un.org/sdgs/dataportal/database  
**Access Method:** Direct CSV download  
**Coverage:** All 17 SDGs, 231 unique indicators  
**Update Frequency:** Quarterly  

**How to Download:**
1. Visit the database portal
2. Select "Country: Ethiopia"
3. Select "All Goals" or specific SDGs
4. Click "Download" → CSV format
5. Save to `data/raw/un_sdg_ethiopia.csv`

### 2. World Bank Open Data
**URL:** https://data.worldbank.org/country/ethiopia  
**API Endpoint:** https://api.worldbank.org/v2/country/ETH/indicator/  
**Coverage:** Economic and social indicators aligned with SDGs  

**Key Indicators to Download:**
- SI.POV.DDAY (Poverty headcount ratio at $2.15 a day)
- SE.PRM.NENR (Primary school enrollment)
- SH.STA.MORT (Infant mortality rate)
- AG.LND.FRST.ZS (Forest area % of land area)
- EG.ELC.ACCS.ZS (Access to electricity)

### 3. UNDP Human Development Reports
**URL:** https://hdr.undp.org/data-center/country-insights#/ranks/ETH  
**Download:** Excel/CSV export  
**Coverage:** HDI, inequality-adjusted metrics  

### 4. Ethiopian Statistical Service (ESS)
**URL:** http://www.statsethiopia.gov.et/  
**Access:** Public PDF reports (manual extraction may be needed)  
**Coverage:** National surveys, census projections  

## Data Validation Checklist
- [ ] All files saved in `data/raw/`
- [ ] File names follow convention: `source_description_date.csv`
- [ ] At least 3 years of historical data per indicator
- [ ] Missing value patterns documented
- [ ] Data licenses allow public use
