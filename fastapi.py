"""
FastAPI REST API example

File: fastapi_rest_api_example.py

This is a minimal, production-oriented example of a REST API using FastAPI.
It demonstrates:
 - Pydantic models for request/response validation
 - Async endpoints
 - CRUD operations (Create, Read, Update, Delete)
 - Error handling with HTTPException
 - Simple in-memory "database" (replaceable with a real DB)
 - CORS middleware example

Dependencies (install with pip):
    pip install fastapi uvicorn[standard] python-multipart

Run the server:
    uvicorn fastapi_rest_api_example:app --reload --port 8000

Sample requests (using curl):
  # Create an item
  curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" \
       -d '{"name": "Example", "description": "An example item", "price": 9.99}'

  # List items
  curl "http://127.0.0.1:8000/items"

  # Get item by id
  curl "http://127.0.0.1:8000/items/1"

  # Update item
  curl -X PUT "http://127.0.0.1:8000/items/1" -H "Content-Type: application/json" \
       -d '{"name": "Updated", "description": "Updated desc", "price": 12.5}'

  # Delete item
  curl -X DELETE "http://127.0.0.1:8000/items/1"

Notes:
 - For a production deployment, use a proper database (Postgres, MySQL, SQLite with SQLAlchemy/SQLModel),
   add authentication/authorization (OAuth2 / JWT), schema migrations, logging, and observability.
 - This example intentionally keeps persistence in-memory for clarity.

"""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

app = FastAPI(title="Example REST API", version="1.0.0")

# Allow CORS for local dev. Adjust origins for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)

class Item(ItemCreate):
    id: UUID

# "In-memory database". Keys are UUIDs stored as strings for simple JSON-friendly output.
_db: dict[str, Item] = {}

# Helper functions
def get_item_or_404(item_id: str) -> Item:
    item = _db.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# CRUD endpoints
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate):
    item_id = str(uuid4())
    item = Item(id=UUID(item_id), **payload.dict())
    # store as string key
    _db[item_id] = item
    return item

@app.get("/items", response_model=List[Item])
async def list_items(limit: int = 100, offset: int = 0):
    # simple pagination
    items = list(_db.values())
    return items[offset : offset + limit]

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = get_item_or_404(item_id)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, payload: ItemCreate):
    existing = get_item_or_404(item_id)
    updated = Item(id=existing.id, **payload.dict())
    _db[item_id] = updated
    return updated

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    # raises 404 if not found
    _ = get_item_or_404(item_id)
    del _db[item_id]
    return None

# Health check and basic metadata
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"service": "example-rest-api", "version": "1.0.0"}
