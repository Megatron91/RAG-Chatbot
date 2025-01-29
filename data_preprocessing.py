import pandas as pd
import re
from nltk.tokenize import sent_tokenize

# Define corpus file path
CORPUS_FILE = "ai_corpus.txt"
OUTPUT_FILE = "chunks.csv"

def clean_text(text):
    """Remove extra spaces and special characters from text."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)  # Remove special characters
    return text.strip()

def chunk_text(text, chunk_size=200):
    """Split long text into smaller chunks (~200-300 words each)."""
    sentences = sent_tokenize(text)
    chunks, current_chunk = [], []
    current_length = 0

    for sentence in sentences:
        current_length += len(sentence.split())
        current_chunk.append(sentence)

        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:  # Add remaining text as a chunk
        chunks.append(" ".join(current_chunk))

    return chunks

# Read AI corpus from the text file
with open(CORPUS_FILE, "r", encoding="utf-8") as file:
    corpus_text = file.read()

# Clean and chunk the text
cleaned_text = clean_text(corpus_text)
chunks = chunk_text(cleaned_text)

# Save processed chunks to a CSV file
df = pd.DataFrame({"chunk_text": chunks})
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Data Preprocessing Complete! {len(chunks)} text chunks saved to {OUTPUT_FILE}.")