"""
ingest.py — HelioBot 3.0
Loads 2022.csv → creates text chunks → embeds → stores in ChromaDB
Run this ONCE before starting the API: python ingest.py
"""

import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import os

CSV_PATH = "data/2022.csv"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "heliobot_colleges"

def load_and_clean(path):
    df = pd.read_csv(path)
    # Use only Round 6 (final cutoffs) for cleaner data
    df = df[df["Round"] == df["Round"].max()]
    df = df.dropna(subset=["Institute", "Academic Program Name", "Closing Rank"])
    df["Closing Rank"] = pd.to_numeric(df["Closing Rank"], errors="coerce")
    df = df.dropna(subset=["Closing Rank"])
    df["Closing Rank"] = df["Closing Rank"].astype(int)
    df["Opening Rank"] = pd.to_numeric(df["Opening Rank"], errors="coerce").fillna(0).astype(int)
    print(f"✅ Loaded {len(df)} rows after cleaning")
    return df

def row_to_text(row):
    """Convert each row into a natural language chunk for embedding."""
    return (
        f"Institute: {row['Institute']}. "
        f"Program: {row['Academic Program Name']}. "
        f"Quota: {row['Quota']}. "
        f"Seat Type: {row['Seat Type']}. "
        f"Gender: {row['Gender']}. "
        f"Opening Rank: {row['Opening Rank']}. "
        f"Closing Rank: {row['Closing Rank']}. "
        f"Year: {row['Year']}."
    )

def ingest():
    print("🚀 Starting ingestion...")

    df = load_and_clean(CSV_PATH)

    # Setup ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Use free local sentence-transformer for embeddings
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Delete old collection if exists (fresh start)
    try:
        client.delete_collection(COLLECTION_NAME)
        print("🗑️ Deleted old collection")
    except:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn
    )

    # Prepare data in batches (ChromaDB limit: 5000 per batch)
    documents = []
    metadatas = []
    ids = []

    for i, (_, row) in enumerate(df.iterrows()):
        documents.append(row_to_text(row))
        metadatas.append({
            "institute": row["Institute"],
            "program": row["Academic Program Name"],
            "quota": row["Quota"],
            "seat_type": row["Seat Type"],
            "gender": row["Gender"],
            "opening_rank": int(row["Opening Rank"]),
            "closing_rank": int(row["Closing Rank"]),
            "year": int(row["Year"])
        })
        ids.append(f"doc_{i}")

    # Batch insert
    BATCH_SIZE = 2000
    total = len(documents)
    for start in range(0, total, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total)
        collection.add(
            documents=documents[start:end],
            metadatas=metadatas[start:end],
            ids=ids[start:end]
        )
        print(f"📥 Inserted {end}/{total} chunks...")

    print(f"\n✅ Ingestion complete! {total} chunks stored in ChromaDB.")
    print(f"📁 Database saved at: {CHROMA_PATH}/")

if __name__ == "__main__":
    ingest()
