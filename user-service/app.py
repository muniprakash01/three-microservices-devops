
from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

DB_PATH = os.getenv("DB_PATH", "/data/users.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "user-service"}), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        with get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            user_id = cursor.lastrowid

        return jsonify({
            "id": user_id,
            "name": name,
            "email": email
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409


@app.route("/users", methods=["GET"])
def get_users():
    with get_db() as conn:
        users = conn.execute("SELECT * FROM users").fetchall()

    return jsonify([dict(user) for user in users]), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    with get_db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user)), 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
