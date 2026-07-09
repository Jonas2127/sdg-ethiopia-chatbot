"""
DAY 2 TASK: Convert UN SDG Excel Files to CSV
This script merges all Goal*.xlsx files into one unified CSV.

Prerequisites: Extract the ZIP to data/raw/un_sdg_raw/
Execute: python scripts/step4b_convert_excel_to_csv.py
"""

import pandas as pd
import os
import glob

print("=" * 60)
print("CONVERTING UN SDG EXCEL FILES TO CSV")
print("=" * 60)

# Source directory with Excel files
source_dir = 'data/raw/un_sdg_raw'
output_file = 'data/raw/un_sdg_ethiopia.csv'

if not os.path.exists(source_dir):
    print(f"\n✗ ERROR: Directory not found: {source_dir}")
    print("\nPlease:")
    print("1. Extract the ZIP file")
    print("2. Create folder: data/raw/un_sdg_raw")
    print("3. Move all Goal*.xlsx files into that folder")
    exit(1)

# Find all Excel files
excel_files = glob.glob(os.path.join(source_dir, 'Goal*.xlsx'))

if not excel_files:
    print(f"\n✗ ERROR: No Goal*.xlsx files found in {source_dir}")
    print("\nMake sure the Excel files are in the un_sdg_raw folder")
    exit(1)

print(f"\nFound {len(excel_files)} Excel files")

all_data = []
errors = []

for filepath in sorted(excel_files):
    filename = os.path.basename(filepath)
    try:
        print(f"  Processing {filename}...", end=" ")
        df = pd.read_excel(filepath)
        
        # Add source file column for tracking
        df['source_file'] = filename
        
        all_data.append(df)
        print(f"✓ ({len(df)} rows)")
        
    except Exception as e:
        print(f"✗ {e}")
        errors.append((filename, str(e)))

if not all_data:
    print("\n✗ ERROR: No data could be read from Excel files")
    exit(1)

# Merge all dataframes
print("\n--- Merging all data ---")
combined_df = pd.concat(all_data, ignore_index=True)

print(f"  Total rows: {len(combined_df):,}")
print(f"  Total columns: {len(combined_df.columns)}")

# Save to CSV
print(f"\n--- Saving to {output_file} ---")
combined_df.to_csv(output_file, index=False, encoding='utf-8')

file_size = os.path.getsize(output_file) / (1024 * 1024)
print(f"  ✓ Saved ({file_size:.2f} MB)")

if errors:
    print("\n⚠ WARNING: Some files had errors:")
    for filename, error in errors:
        print(f"  - {filename}: {error}")

print("\n" + "=" * 60)
print("CONVERSION COMPLETE")
print("=" * 60)
print(f"\nOutput file: {output_file}")
print(f"Total records: {len(combined_df):,}")
print("\nNext step: python scripts/step4_verify_data.py")
