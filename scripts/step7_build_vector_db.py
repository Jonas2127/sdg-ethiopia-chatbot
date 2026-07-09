"""
DAY 5 TASK: Build Vector Database with ChromaDB
Creates embeddings and stores them for semantic search.

Execute: python scripts/step7_build_vector_db.py
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer
import os
from tqdm import tqdm

print("=" * 60)
print("BUILDING VECTOR DATABASE")
print("=" * 60)

# ============================================
# PART 1: Load Knowledge Base
# ============================================
print("\n[1/4] Loading knowledge base...")

docs_file = 'data/processed/knowledge_base/documents.jsonl'
documents = []
metadatas = []
ids = []

with open(docs_file, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        entry = json.loads(line)
        documents.append(entry['text'])
        metadatas.append(entry['metadata'])
        ids.append(f"doc_{idx}")

print(f"  ✓ Loaded {len(documents):,} documents")

# ============================================
# PART 2: Initialize Embedding Model
# ============================================
print("\n[2/4] Loading embedding model...")
print("  (First run will download ~400MB model - be patient)")

model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"  ✓ Model loaded: all-MiniLM-L6-v2")

# ============================================
# PART 3: Create ChromaDB Collection
# ============================================
print("\n[3/4] Creating vector database...")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Delete existing collection if it exists
try:
    chroma_client.delete_collection(name="ethiopia_sdg")
    print("  ⚠ Deleted existing collection")
except:
    pass

# Create new collection
collection = chroma_client.create_collection(
    name="ethiopia_sdg",
    metadata={"description": "Ethiopia SDG indicators and statistics"}
)

print(f"  ✓ Collection created: ethiopia_sdg")


# ============================================
# PART 4: Generate Embeddings & Add to DB
# ============================================
print("\n[4/4] Generating embeddings and storing...")
print("  This may take 5-10 minutes for 11,346 documents")

batch_size = 100
total_batches = (len(documents) + batch_size - 1) // batch_size

for i in range(0, len(documents), batch_size):
    batch_docs = documents[i:i+batch_size]
    batch_metas = metadatas[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    
    # Generate embeddings for this batch
    embeddings = model.encode(batch_docs, show_progress_bar=False)
    
    # Add to ChromaDB
    collection.add(
        documents=batch_docs,
        metadatas=batch_metas,
        embeddings=embeddings.tolist(),
        ids=batch_ids
    )
    
    # Progress update
    current_batch = (i // batch_size) + 1
    print(f"  Batch {current_batch}/{total_batches} complete ({i+len(batch_docs):,} / {len(documents):,} docs)")

print(f"\n  ✓ All {len(documents):,} documents embedded and stored")

# ============================================
# PART 5: Test the Database
# ============================================
print("\n[5/5] Testing vector search...")

test_query = "What is Ethiopia's poverty rate?"
query_embedding = model.encode([test_query])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3
)

print(f"\nTest Query: '{test_query}'")
print(f"\nTop 3 Results:")
for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    print(f"\n  Result {i+1}:")
    print(f"    Indicator: {meta.get('indicator', 'N/A')}")
    print(f"    Year: {meta.get('time_period', 'N/A')}")
    print(f"    Value: {meta.get('obs_value', 'N/A')}")

print("\n" + "=" * 60)
print("VECTOR DATABASE BUILT SUCCESSFULLY")
print("=" * 60)
print(f"\nDatabase location: ./chroma_db")
print(f"Total documents: {len(documents):,}")
print(f"Embedding model: all-MiniLM-L6-v2")
print(f"Vector dimensions: 384")
print(f"\nNext step: python scripts\\step8_build_chatbot.py")
