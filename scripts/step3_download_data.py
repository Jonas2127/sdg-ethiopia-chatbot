"""
DAY 2 TASK: Download SDG Data for Ethiopia
This script downloads Ethiopia SDG data from UN and World Bank sources.

Execute: python scripts/step3_download_data.py
"""

import pandas as pd
import requests
import os
from datetime import datetime

print("=" * 60)
print("DOWNLOADING ETHIOPIA SDG DATA")
print("=" * 60)

# Create data directory if it doesn't exist
os.makedirs('data/raw', exist_ok=True)

# ============================================
# PART 1: World Bank Data via API
# ============================================
print("\n[1/2] Downloading World Bank indicators...")

# Key SDG-related indicators for Ethiopia
wb_indicators = {
    'SI.POV.DDAY': 'poverty_headcount',
    'SE.PRM.NENR': 'primary_enrollment',
    'SH.STA.MORT': 'infant_mortality',
    'EG.ELC.ACCS.ZS': 'electricity_access',
    'AG.LND.FRST.ZS': 'forest_area',
}

all_wb_data = []

for indicator_code, indicator_name in wb_indicators.items():
    try:
        url = f"https://api.worldbank.org/v2/country/ETH/indicator/{indicator_code}?format=json&per_page=100"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1]:
                for entry in data[1]:
                    all_wb_data.append({
                        'indicator_code': indicator_code,
                        'indicator_name': indicator_name,
                        'year': entry.get('date'),
                        'value': entry.get('value'),
                        'country': 'Ethiopia'
                    })
                print(f"  ✓ {indicator_name}: {len(data[1])} records")
            else:
                print(f"  ✗ {indicator_name}: No data available")
        else:
            print(f"  ✗ {indicator_name}: API error {response.status_code}")
    except Exception as e:
        print(f"  ✗ {indicator_name}: {e}")

# Save World Bank data
if all_wb_data:
    df_wb = pd.DataFrame(all_wb_data)
    output_file = 'data/raw/worldbank_ethiopia_sdg.csv'
    df_wb.to_csv(output_file, index=False)
    print(f"\n✓ Saved {len(df_wb)} World Bank records to {output_file}")
else:
    print("\n✗ No World Bank data downloaded")

# ============================================
# PART 2: Manual UN Data Instructions
# ============================================
print("\n[2/2] UN SDG Database (Manual Download Required)")
print("\nThe UN SDG database requires manual download. Follow these steps:")
print("\n1. Visit: https://unstats.un.org/sdgs/dataportal/database")
print("2. Click 'Country or Area' → Select 'Ethiopia'")
print("3. Select 'All Goals' or specific SDGs")
print("4. Click 'Download' button → Choose 'CSV' format")
print("5. Save the file as: data/raw/un_sdg_ethiopia.csv")
print("\nAfter downloading, run: python scripts/step4_clean_data.py")

print("\n" + "=" * 60)
print("DATA DOWNLOAD SUMMARY")
print("=" * 60)
print(f"✓ World Bank data: Automated download complete")
print(f"⚠ UN SDG data: Manual download required (see instructions above)")
print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
