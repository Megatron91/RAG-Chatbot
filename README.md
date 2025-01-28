# 🧠 RAG Chatbot - Retrieval-Augmented Generation Chatbot

This is a **Retrieval-Augmented Generation (RAG) Chatbot** that retrieves relevant text chunks using **FAISS** and generates responses based on a **vector database**.

## 🌟 Features
- **Text Chunking & Embeddings**: Uses `sentence-transformers` to generate embeddings.
- **FAISS for Semantic Search**: Stores and retrieves text using FAISS.
- **Flask API**: Exposes chat and history retrieval endpoints.
- **SQLite for Chat History**: Stores past conversations.

## 🚀 Setup & Usage
### **1. Install Dependencies**
    ```bash
    pip install -r requirements.txt
