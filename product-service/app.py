
from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

DB_PATH = os.getenv("DB_PATH", "/data/products.db")


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "product-service"}), 200


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    price = data.get("price")

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    try:
        price = float(price)
        if price < 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"error": "Price must be a non-negative number"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            (name, price)
        )
        product_id = cursor.lastrowid

    return jsonify({
        "id": product_id,
        "name": name,
        "price": price
    }), 201


@app.route("/products", methods=["GET"])
def get_products():
    with get_db() as conn:
        products = conn.execute("SELECT * FROM products").fetchall()

    return jsonify([dict(product) for product in products]), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    with get_db() as conn:
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(dict(product)), 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
