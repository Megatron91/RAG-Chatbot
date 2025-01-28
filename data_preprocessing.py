import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a sample dataset or scrape/copy some text documents
documents = [
    "Artificial Intelligence is transforming industries.",
    "Natural Language Processing allows machines to understand human language.",
    "Machine Learning models are trained using data.",
    "Deep Learning improves model accuracy in NLP and vision tasks.",
]

# Define the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Split documents into smaller chunks (if necessary)
chunk_size = 200  # Approximate token size
chunks = []
for doc in documents:
    words = doc.split()
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

# Generate embeddings
embeddings = model.encode(chunks)

# Store embeddings in Faiss
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 norm distance
index.add(np.array(embeddings, dtype=np.float32))

# Save the Faiss index
faiss.write_index(index, "vector_store.faiss")

# Save text chunks
pd.DataFrame({"chunk": chunks}).to_csv("chunks.csv", index=False)

print("Data preprocessing complete. Embeddings stored.")
