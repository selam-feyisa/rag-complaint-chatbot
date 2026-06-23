import pandas as pd
import chromadb
from tqdm import tqdm
import os

print("🔄 Rebuilding ChromaDB...")

# Find the file
possible_paths = [
    'data/processed/filtered_complaints.csv',
    'filtered_complaints.csv',
    'notebooks/data/processed/filtered_complaints.csv'
]

file_path = None
for path in possible_paths:
    if os.path.exists(path):
        file_path = path
        break

if not file_path:
    raise FileNotFoundError("Could not find filtered_complaints.csv")

print(f"✅ Found file at: {file_path}")

df = pd.read_csv(file_path, nrows=6000)
print(f"Loaded {len(df):,} complaints")

# Chunking
chunks = []
metadatas = []

for idx, row in tqdm(df.iterrows(), total=len(df)):
    text = str(row.get('cleaned_narrative', ''))
    if len(text.strip()) > 50:
        chunks.append(text[:950])
        metadatas.append({
            "product_category": str(row.get('Product', 'Unknown')),
            "issue": str(row.get('Issue', 'General')),
            "complaint_id": str(row.get('Complaint ID', idx))
        })

print(f"Created {len(chunks)} chunks")

# Rebuild ChromaDB with smaller batches
client = chromadb.PersistentClient(path="vector_store/chroma_db")

try:
    client.delete_collection("complaints")
except:
    pass

collection = client.create_collection("complaints")

# Add in smaller batches to avoid error
batch_size = 2000
for i in tqdm(range(0, len(chunks), batch_size)):
    end = min(i + batch_size, len(chunks))
    batch_chunks = chunks[i:end]
    batch_meta = metadatas[i:end]
    batch_ids = [f"chunk_{j}" for j in range(i, end)]
    
    collection.add(
        documents=batch_chunks,
        metadatas=batch_meta,
        ids=batch_ids
    )
    print(f"Added batch {i//batch_size + 1} / {len(chunks)//batch_size + 1}")

print("🎉✅ Vector Store Rebuilt Successfully!")