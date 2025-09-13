"""
Flask REST API example

File: flask_rest_api_example.py

This is a minimal REST API built with Flask.
It demonstrates:
 - CRUD operations (Create, Read, Update, Delete)
 - Request/response handling
 - JSON input/output
 - Error handling with proper HTTP codes
 - Simple in-memory storage

Dependencies (install with pip):
    pip install flask

Run the server:
    python flask_rest_api_example.py

Sample requests (using curl):
  # Create an item
  curl -X POST "http://127.0.0.1:5000/items" -H "Content-Type: application/json" \
       -d '{"name": "Example", "description": "An example item", "price": 9.99}'

  # List items
  curl "http://127.0.0.1:5000/items"

  # Get item by id
  curl "http://127.0.0.1:5000/items/1"

  # Update item
  curl -X PUT "http://127.0.0.1:5000/items/1" -H "Content-Type: application/json" \
       -d '{"name": "Updated", "description": "Updated desc", "price": 12.5}'

  # Delete item
  curl -X DELETE "http://127.0.0.1:5000/items/1"

Notes:
 - For production, consider using Flask-RESTful or Flask-Smorest, a real database, authentication, and error logging.
"""

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory database (dictionary)
_db = {}
_counter = 1

# Helper
def get_item_or_404(item_id: int):
    item = _db.get(item_id)
    if not item:
        abort(404, description="Item not found")
    return item

# Routes
@app.route("/", methods=["GET"])
def root():
    return {"service": "flask-rest-api", "version": "1.0.0"}

@app.route("/items", methods=["POST"])
def create_item():
    global _counter
    data = request.get_json(force=True)
    if not data or "name" not in data or "price" not in data:
        abort(400, description="Invalid input. 'name' and 'price' required.")

    item = {
        "id": _counter,
        "name": data["name"],
        "description": data.get("description"),
        "price": data["price"]
    }
    _db[_counter] = item
    _counter += 1
    return jsonify(item), 201

@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(list(_db.values()))

@app.route("/items/<int:item_id>", methods=["GET"])
def read_item(item_id):
    item = get_item_or_404(item_id)
    return jsonify(item)

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = get_item_or_404(item_id)
    data = request.get_json(force=True)
    if not data or "name" not in data or "price" not in data:
        abort(400, description="Invalid input. 'name' and 'price' required.")

    item.update({
        "name": data["name"],
        "description": data.get("description"),
        "price": data["price"]
    })
    _db[item_id] = item
    return jsonify(item)

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = get_item_or_404(item_id)
    del _db[item_id]
    return "", 204

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
