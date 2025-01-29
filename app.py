from flask import Flask, request, jsonify
import sqlite3
import datetime
from rag_chatbot import generate_response

# Initialize Flask app
app = Flask(__name__)

# Database helper function
def get_db_connection():
    """Create a new database connection per request."""
    conn = sqlite3.connect("chat_history.db")
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# Ensure database table exists
def initialize_database():
    """Create chat history table if it does not exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            role TEXT,
            content TEXT
        )
        """)
        conn.commit()

# Initialize DB at startup
initialize_database()

@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to the RAG-Chatbot API</h1><p>Use /chat to ask a question or /history to see past chats.</p>"

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages by retrieving relevant responses."""
    try:
        data = request.get_json()
        if not data or "query" not in data or not data["query"].strip():
            return jsonify({"error": "Missing or empty 'query' field"}), 400

        query = data["query"].strip()
        response = generate_response(query)

        # Store chat in database
        timestamp = datetime.datetime.now().isoformat()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO chat_history (timestamp, role, content) VALUES (?, ?, ?)",
                [(timestamp, "user", query), (timestamp, "bot", response)]
            )
            conn.commit()

        return jsonify({"query": query, "response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message

@app.route("/history", methods=["GET"])
def get_history():
    """Retrieve chat history from the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, role, content FROM chat_history ORDER BY timestamp DESC")
            history = [{"id": row["id"], "timestamp": row["timestamp"], "role": row["role"], "content": row["content"]} for row in cursor.fetchall()]
        
        return jsonify({"history": history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors gracefully

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)  # Disable debug in production