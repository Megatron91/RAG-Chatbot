import faiss
import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from collections import Counter

# Define file paths
FAISS_INDEX_FILE = "vector_store.faiss"
CHUNKS_FILE = "chunks.csv"

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Check if necessary files exist
if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(CHUNKS_FILE):
    raise FileNotFoundError("FAISS index or chunks.csv is missing! Run `embed_store.py` first.")

# Load stored FAISS index and text chunks
index = faiss.read_index(FAISS_INDEX_FILE)
chunks_df = pd.read_csv(CHUNKS_FILE)
chunks = chunks_df["chunk_text"].tolist()

def retrieve_top_chunks(query, top_k=3):
    #Retrieve the most relevant text chunks using FAISS similarity search.
    if not query.strip():
        return ["[No valid input provided.]"]

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype=np.float32)

    # Normalize FAISS search for better similarity
    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, top_k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]

def summarize_chunks(chunks):
    #Summarize retrieved chunks into a readable response.
    if not chunks:
        return "I couldn't find relevant information."

    # Extract the most frequently occurring words for better summarization
    words = " ".join(chunks).split()
    word_counts = Counter(words)
    top_words = [word for word, count in word_counts.most_common(10)]

    # Create a readable response with a short summary
    summary = f"{chunks[0][:500]}... (truncated)"

    # for chunk in chunks[1:3]:  # Show top 3 relevant points
    #     summary += f"{chunk[:200]}...\n"  # Truncate for readability

    return summary

def generate_response(query):
    #Retrieve relevant chunks and generate a structured response.
    retrieved_chunks = retrieve_top_chunks(query)
    return summarize_chunks(retrieved_chunks)

if __name__ == "__main__":
    print("RAG Chatbot Initialized! Type 'exit' to quit.\n")
    while True:
        query = input("User: ")
        if query.lower() in ["exit", "quit"]:
            print("Exiting chatbot. Goodbye!")
            break
        response = generate_response(query)
        print(f"\n Bot:\n{response}\n")