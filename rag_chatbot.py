import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the stored FAISS index and text chunks
index = faiss.read_index("vector_store.faiss")
chunks_df = pd.read_csv("chunks.csv")
chunks = chunks_df["chunk"].tolist()

def retrieve_top_chunks(query, top_k=3):
    """Retrieve the most relevant text chunks using vector similarity."""
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), top_k)
    return [chunks[i] for i in indices[0]]

def generate_response(query):
    """Retrieve relevant chunks and generate a response."""
    retrieved_chunks = retrieve_top_chunks(query)
    return " ".join(retrieved_chunks)

if __name__ == "__main__":
    while True:
        query = input("User: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = generate_response(query)
        print(f"Bot: {response}")
