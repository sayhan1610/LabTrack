from fastapi import APIRouter
from models.items import Item
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

route = APIRouter()

# Get Request Method
@route.get("/")
async def get_items():
    items = list_serial(collection_name.find())
    return items

# Post Request Method
@route.post("/")
async def create_items(item: Item):
    # Convert Pydantic model to dictionary using .dict() method
    item_dict = item.dict()
    # Insert item into collection
    collection_name.insert_one(item_dict)
    return {"message": "Item created successfully"}

# Put Request Method
@route.put("/{id}")
async def update_items(id: str, item: Item):
    # Convert Pydantic model to dictionary using .dict() method
    item_dict = item.dict()
    # Update item in collection
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": item_dict})
    return {"message": "Item updated successfully"}

# Delete Request Method
@route.delete("/{id}")
async def delete_items(id: str):
    # Delete item from collection
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "Item deleted successfully"} 
