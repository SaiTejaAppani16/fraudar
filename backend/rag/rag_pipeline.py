import chromadb
from backend.rag.seed_data import SCAM_PATTERNS

# Initialize ChromaDB client with persistent storage
client = chromadb.PersistentClient(path="./data/chromadb")

def get_or_create_collection():
    """
    Gets existing scam patterns collection or creates it if it doesn't exist.
    """
    return client.get_or_create_collection(
        name="scam_patterns",
        metadata={"hnsw:space": "cosine"}
    )

def seed_database():
    """
    Seeds ChromaDB with known scam patterns from FTC and FBI IC3 data.
    Only adds patterns that don't already exist — safe to run multiple times.
    """
    collection = get_or_create_collection()
    
    existing = collection.get()
    existing_ids = set(existing["ids"])
    
    new_patterns = [p for p in SCAM_PATTERNS if p["id"] not in existing_ids]
    
    if not new_patterns:
        print("Database already seeded. Skipping.")
        return
    
    collection.add(
        ids=[p["id"] for p in new_patterns],
        documents=[p["text"] for p in new_patterns],
        metadatas=[p["metadata"] for p in new_patterns]
    )
    
    print(f"Seeded {len(new_patterns)} scam patterns into ChromaDB.")

def search_similar_scams(text: str, n_results: int = 3) -> list:
    """
    Searches ChromaDB for scam patterns similar to the input text.
    Returns the top N most similar known scams with their metadata.
    """
    collection = get_or_create_collection()
    
    results = collection.query(
        query_texts=[text],
        n_results=n_results
    )
    
    similar_scams = []
    for i, doc in enumerate(results["documents"][0]):
        similar_scams.append({
            "pattern": doc,
            "scam_type": results["metadatas"][0][i]["type"],
            "source": results["metadatas"][0][i]["source"],
            "similarity_score": round(1 - results["distances"][0][i], 3)
        })
    
    return similar_scams


def initialize_rag():
    """
    Called at app startup to ensure database is seeded and ready.
    """
    seed_database()
    print("RAG pipeline initialized.")