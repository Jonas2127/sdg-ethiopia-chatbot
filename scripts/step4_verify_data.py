"""
DAY 2 TASK: Verify Downloaded Data
This script checks that your data files are valid and ready for processing.

Execute: python scripts/step4_verify_data.py
"""

import pandas as pd
import os

print("=" * 60)
print("DATA VERIFICATION")
print("=" * 60)

data_dir = 'data/raw'
required_files = {
    'worldbank_ethiopia_sdg.csv': 'World Bank Indicators',
    'un_sdg_ethiopia.csv': 'UN SDG Database'
}

all_good = True

for filename, description in required_files.items():
    filepath = os.path.join(data_dir, filename)
    
    print(f"\n[{description}]")
    print(f"File: {filename}")
    
    if not os.path.exists(filepath):
        print(f"  ✗ NOT FOUND")
        print(f"  Expected location: {filepath}")
        all_good = False
        continue
    
    try:
        df = pd.read_csv(filepath)
        file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
        
        print(f"  ✓ File exists ({file_size:.2f} MB)")
        print(f"  ✓ Rows: {len(df):,}")
        print(f"  ✓ Columns: {len(df.columns)}")
        print(f"  Column names: {', '.join(df.columns[:5].tolist())}" + 
              (f"... (+{len(df.columns)-5} more)" if len(df.columns) > 5 else ""))
        
    except Exception as e:
        print(f"  ✗ ERROR reading file: {e}")
        all_good = False

print("\n" + "=" * 60)
if all_good:
    print("✓ ALL DATA FILES VERIFIED")
    print("=" * 60)
    print("\nYou're ready for Day 3: Data Cleaning!")
    print("Next step: python scripts/step5_clean_data.py")
else:
    print("⚠ SOME FILES MISSING OR INVALID")
    print("=" * 60)
    print("\nPlease complete the data download steps.")
