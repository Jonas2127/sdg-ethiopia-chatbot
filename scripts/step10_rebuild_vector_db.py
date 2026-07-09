"""
Step 10: Rebuild Vector Database (Add ESS Reports)
Combines existing UN/World Bank data with new ESS reports

Usage: python scripts/step10_rebuild_vector_db.py
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer
import os

print("=" * 60)
print("REBUILDING VECTOR DATABASE WITH ESS REPORTS")
print("=" * 60)

# Load embedding model
print("\n[1/5] Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✓ Model loaded")

# Connect to ChromaDB
print("\n[2/5] Connecting to database...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Delete old collection if exists
try:
    chroma_client.delete_collection(name="ethiopia_sdg")
    print("✓ Deleted old collection")
except:
    pass

# Create new collection
collection = chroma_client.create_collection(
    name="ethiopia_sdg",
    metadata={"description": "Ethiopia SDG data + ESS reports"}
)
print("✓ Created new collection")

# Load original knowledge base (UN + World Bank)
print("\n[3/5] Loading original knowledge base...")
original_kb_path = "data/processed/knowledge_base/documents.jsonl"

original_documents = []
if os.path.exists(original_kb_path):
    with open(original_kb_path, 'r', encoding='utf-8') as f:
        for line in f:
            original_documents.append(json.loads(line))
    print(f"✓ Loaded {len(original_documents)} original documents")
else:
    print("✗ Original knowledge base not found!")
    exit(1)

# Load ESS documents
print("\n[4/5] Loading ESS reports...")
ess_kb_path = "data/processed/ess_documents.jsonl"

ess_documents = []
if os.path.exists(ess_kb_path):
    with open(ess_kb_path, 'r', encoding='utf-8') as f:
        for line in f:
            ess_documents.append(json.loads(line))
    print(f"✓ Loaded {len(ess_documents)} ESS document chunks")
else:
    print("⚠ No ESS documents found. Run step9_process_ess_reports.py first")
    print("Continuing with original data only...")

# Combine all documents
all_documents = original_documents + ess_documents
print(f"\n✓ Total documents: {len(all_documents)}")
print(f"  - Original (UN/World Bank): {len(original_documents)}")
print(f"  - ESS Reports: {len(ess_documents)}")

# Add to vector database in batches
print("\n[5/5] Building vector database...")
batch_size = 100
total_batches = (len(all_documents) + batch_size - 1) // batch_size

for i in range(0, len(all_documents), batch_size):
    batch = all_documents[i:i + batch_size]
    
    # Extract texts and metadata
    texts = [doc['text'] for doc in batch]
    metadatas = [doc.get('metadata', {}) for doc in batch]
    ids = [f"doc_{i + j}" for j in range(len(batch))]
    
    # Generate embeddings
    embeddings = embedding_model.encode(texts).tolist()
    
    # Add to collection
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    current_batch = (i // batch_size) + 1
    print(f"  Processed batch {current_batch}/{total_batches} ({len(batch)} docs)")

print("\n" + "=" * 60)
print("✓ VECTOR DATABASE REBUILT SUCCESSFULLY")
print("=" * 60)
print(f"Database location: ./chroma_db")
print(f"Total documents: {len(all_documents)}")
print(f"  - UN/World Bank: {len(original_documents)}")
print(f"  - ESS Reports: {len(ess_documents)}")
print(f"Embedding model: all-MiniLM-L6-v2")
print(f"Vector dimensions: 384")
print("\n" + "=" * 60)
print("NEXT STEP:")
print("=" * 60)
print("Run your chatbot: python -m streamlit run app.py")
print("\nYour chatbot now includes ESS reports!")
print("=" * 60)
