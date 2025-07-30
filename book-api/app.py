from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Get MongoDB credentials from environment variables (Kubernetes will inject these)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "bookdb")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
books_collection = db.books

@app.route('/')
def home():
    return "Book API is running! Use /books for operations."

# ✅ GET all books
@app.route('/books', methods=['GET'])
def get_books():
    books = list(books_collection.find({}, {'_id': 0}))
    return jsonify(books)

# ✅ GET one book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = books_collection.find_one({'id': book_id}, {'_id': 0})
    return jsonify(book) if book else ("Book not found", 404)

# ✅ POST add new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    latest = books_collection.find_one(sort=[("id", -1)])
    next_id = (latest["id"] + 1) if latest else 1
    new_book = {
        "id": next_id,
        "title": data["title"],
        "author": data["author"]
    }
    books_collection.insert_one(new_book)

    # Return a clean response without MongoDB _id
    return jsonify({
        "message": "Book added!",
        "book": new_book
    }), 201

# ✅ PUT update book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    update = {
        "$set": {
            "title": data.get("title"),
            "author": data.get("author")
        }
    }
    result = books_collection.update_one({"id": book_id}, update)
    if result.matched_count == 0:
        return ("Book not found", 404)
    updated_book = books_collection.find_one({'id': book_id}, {'_id': 0})
    return jsonify(updated_book)

# ✅ DELETE remove book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = books_collection.delete_one({'id': book_id})
    if result.deleted_count == 0:
        return ("Book not found", 404)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
