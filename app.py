from flask import Flask, request, jsonify
import sqlite3
import datetime
from rag_chatbot import generate_response

# Initialize Flask app
app = Flask(__name__)

# Set up SQLite database for chat history
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
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

@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to the RAG-Chatbot API</h1><p>Use the /chat or /history endpoint to get response.</p>"


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages by retrieving relevant responses."""
    data = request.get_json()
    if "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    query = data["query"]
    response = generate_response(query)

    # Store in database
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO chat_history (timestamp, role, content) VALUES (?, ?, ?)", (timestamp, "user", query))
    cursor.execute("INSERT INTO chat_history (timestamp, role, content) VALUES (?, ?, ?)", (timestamp, "bot", response))
    conn.commit()

    return jsonify({"query": query, "response": response})

@app.route("/history", methods=["GET"])
def get_history():
    """Retrieve chat history from the database."""
    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC")
    history = cursor.fetchall()
    return jsonify(history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
