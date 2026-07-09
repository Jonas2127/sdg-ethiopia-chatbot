"""
DAY 4 TASK: Create Knowledge Base for RAG System
Converts cleaned data into text chunks that the chatbot can search.

Execute: python scripts/step6_create_knowledge_base.py
"""

import pandas as pd
import os
import json

print("=" * 60)
print("CREATING KNOWLEDGE BASE")
print("=" * 60)

# Load cleaned data
df = pd.read_csv('data/processed/ethiopia_sdg_clean.csv')
print(f"\nLoaded {len(df):,} records")

# ============================================
# PART 1: Create Text Documents
# ============================================
print("\n[1/3] Converting data to text documents...")

documents = []
metadata_list = []

for idx, row in df.iterrows():
    indicator = str(row.get('indicator', 'Unknown'))
    time_period = str(row.get('time_period', 'Unknown'))
    obs_value = row.get('obs_value', 'N/A')
    data_source = str(row.get('data_source', 'Unknown'))
    
    text = f"""Indicator: {indicator}
Year: {time_period}
Value: {obs_value}
Country: Ethiopia
Data Source: {data_source}

Context: In {time_period}, Ethiopia's {indicator} was {obs_value}. This data comes from {data_source} and relates to the UN Sustainable Development Goals."""
    
    documents.append(text)
    metadata_list.append({
        'indicator': indicator,
        'time_period': time_period,
        'obs_value': str(obs_value),
        'data_source': data_source,
        'doc_id': f"doc_{idx}"
    })
    
    if (idx + 1) % 1000 == 0:
        print(f"  Processed {idx + 1:,} / {len(df):,} records...")

print(f"  ✓ Created {len(documents):,} text documents")

# ============================================
# PART 2: Save Knowledge Base
# ============================================
print("\n[2/3] Saving knowledge base...")

os.makedirs('data/processed/knowledge_base', exist_ok=True)

docs_file = 'data/processed/knowledge_base/documents.jsonl'
with open(docs_file, 'w', encoding='utf-8') as f:
    for doc, meta in zip(documents, metadata_list):
        entry = {'text': doc, 'metadata': meta}
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

print(f"  ✓ Saved {len(documents):,} documents to {docs_file}")

meta_file = 'data/processed/knowledge_base/metadata.json'
with open(meta_file, 'w', encoding='utf-8') as f:
    json.dump(metadata_list, f, indent=2, ensure_ascii=False)

print(f"  ✓ Saved metadata to {meta_file}")

# ============================================
# PART 3: Create Summary Statistics
# ============================================
print("\n[3/3] Generating statistics...")

total_docs = len(documents)
unique_indicators = df['indicator'].nunique() if 'indicator' in df.columns else 0
time_range = df['time_period'].agg(['min', 'max']) if 'time_period' in df.columns else None
avg_doc_length = sum(len(doc) for doc in documents) / len(documents)

stats = {
    'total_documents': total_docs,
    'unique_indicators': int(unique_indicators),
    'time_period_range': {
        'earliest': str(time_range['min']) if time_range is not None else 'Unknown',
        'latest': str(time_range['max']) if time_range is not None else 'Unknown'
    },
    'average_document_length': int(avg_doc_length),
    'data_sources': df['data_source'].value_counts().to_dict() if 'data_source' in df.columns else {}
}

stats_file = 'data/processed/knowledge_base/stats.json'
with open(stats_file, 'w', encoding='utf-8') as f:
    json.dump(stats, f, indent=2)

print(f"  ✓ Saved statistics to {stats_file}")

print("\n" + "=" * 60)
print("KNOWLEDGE BASE CREATED")
print("=" * 60)
print(f"\nSummary:")
print(f"  Total documents: {total_docs:,}")
print(f"  Unique indicators: {unique_indicators}")
print(f"  Time period: {stats['time_period_range']['earliest']} - {stats['time_period_range']['latest']}")
print(f"  Average document length: {int(avg_doc_length)} characters")
print(f"\nData sources:")
for source, count in stats['data_sources'].items():
    print(f"  - {source}: {count:,} records")

print(f"\nNext step: python scripts\\step7_build_vector_db.py")
