"""
DAY 3 TASK: Clean and Standardize SDG Data
This script cleans both datasets and prepares them for the chatbot.

Execute: python scripts/step5_clean_data.py
"""

import pandas as pd
import os

print("=" * 60)
print("DATA CLEANING & STANDARDIZATION")
print("=" * 60)

# Create output directory
os.makedirs('data/processed', exist_ok=True)

# ============================================
# PART 1: Clean World Bank Data
# ============================================
print("\n[1/3] Cleaning World Bank data...")

wb_df = pd.read_csv('data/raw/worldbank_ethiopia_sdg.csv')
print(f"  Original: {len(wb_df)} rows, {len(wb_df.columns)} columns")

# Remove rows with missing values
wb_df_clean = wb_df.dropna(subset=['value'])
print(f"  After removing missing values: {len(wb_df_clean)} rows")

# Standardize column names
wb_df_clean = wb_df_clean.rename(columns={
    'indicator_name': 'indicator',
    'year': 'time_period',
    'value': 'obs_value',
    'country': 'geo_area_name'
})

# Add source column
wb_df_clean['data_source'] = 'World Bank'

print(f"  ✓ World Bank data cleaned")

# ============================================
# PART 2: Clean UN SDG Data
# ============================================
print("\n[2/3] Cleaning UN SDG data...")

un_df = pd.read_csv('data/raw/un_sdg_ethiopia.csv')
print(f"  Original: {len(un_df)} rows, {len(un_df.columns)} columns")

# Show column names to understand structure
print(f"  Columns: {', '.join(un_df.columns.tolist()[:10])}")
if len(un_df.columns) > 10:
    print(f"           ... (+{len(un_df.columns)-10} more)")

# Common UN SDG column names to look for
value_cols = ['Value', 'OBS_VALUE', 'value', 'obs_value']
time_cols = ['Time', 'TimePeriod', 'time_period', 'Year', 'year']
indicator_cols = ['Indicator', 'SeriesDescription', 'indicator']

# Find actual column names (case-insensitive)
actual_value_col = None
actual_time_col = None
actual_indicator_col = None

for col in un_df.columns:
    if col in value_cols or col.lower() in [v.lower() for v in value_cols]:
        actual_value_col = col
    if col in time_cols or col.lower() in [t.lower() for t in time_cols]:
        actual_time_col = col
    if col in indicator_cols or col.lower() in [i.lower() for i in indicator_cols]:
        actual_indicator_col = col

print(f"  Detected value column: {actual_value_col}")
print(f"  Detected time column: {actual_time_col}")
print(f"  Detected indicator column: {actual_indicator_col}")

# Clean based on detected columns
if actual_value_col:
    un_df_clean = un_df.dropna(subset=[actual_value_col])
    print(f"  After removing missing values: {len(un_df_clean)} rows")
else:
    un_df_clean = un_df
    print(f"  ⚠ Could not find value column, keeping all rows")

# Standardize column names
rename_map = {}
if actual_value_col:
    rename_map[actual_value_col] = 'obs_value'
if actual_time_col:
    rename_map[actual_time_col] = 'time_period'
if actual_indicator_col:
    rename_map[actual_indicator_col] = 'indicator'

un_df_clean = un_df_clean.rename(columns=rename_map)

# Add source column
un_df_clean['data_source'] = 'UN SDG Database'
un_df_clean['geo_area_name'] = 'Ethiopia'

print(f"  ✓ UN SDG data cleaned")

# ============================================
# PART 3: Combine & Save
# ============================================
print("\n[3/3] Combining datasets...")

# Select common columns for merging
common_columns = ['indicator', 'time_period', 'obs_value', 'geo_area_name', 'data_source']

# Keep only columns that exist in both
wb_cols_to_keep = [col for col in common_columns if col in wb_df_clean.columns]
un_cols_to_keep = [col for col in common_columns if col in un_df_clean.columns]

wb_subset = wb_df_clean[wb_cols_to_keep]
un_subset = un_df_clean[un_cols_to_keep]

# Combine
combined_df = pd.concat([wb_subset, un_subset], ignore_index=True)

print(f"  Combined: {len(combined_df)} total rows")
print(f"  Columns: {', '.join(combined_df.columns.tolist())}")

# Save cleaned datasets
output_file = 'data/processed/ethiopia_sdg_clean.csv'
combined_df.to_csv(output_file, index=False)

file_size = os.path.getsize(output_file) / (1024 * 1024)
print(f"\n  ✓ Saved to: {output_file}")
print(f"  File size: {file_size:.2f} MB")

# Save individual cleaned files too
wb_df_clean.to_csv('data/processed/worldbank_clean.csv', index=False)
un_df_clean.to_csv('data/processed/un_sdg_clean.csv', index=False)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETE")
print("=" * 60)
print(f"\nCleaned data summary:")
print(f"  World Bank: {len(wb_df_clean):,} records")
print(f"  UN SDG: {len(un_df_clean):,} records")
print(f"  Combined: {len(combined_df):,} records")
print(f"\nNext step: python scripts/step6_create_knowledge_base.py")
