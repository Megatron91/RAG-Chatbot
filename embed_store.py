import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load text chunks
chunks_df = pd.read_csv("chunks.csv")
chunks = chunks_df["chunk"].tolist()

# Generate embeddings
embeddings = model.encode(chunks)

# Initialize FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance index
index.add(np.array(embeddings, dtype=np.float32))

# Save the index to disk
faiss.write_index(index, "vector_store.faiss")

print("Embeddings stored successfully in vector_store.faiss")
