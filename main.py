from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import Query
from bson.errors import InvalidId
import os

# Initialize FastAPI app
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware configuration
# Allows requests from any origin. For production, you should replace "*" with specific domains that need access.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# MongoDB configuration
# Update `MONGO_DETAILS` with your MongoDB connection string.
MONGO_DETAILS = os.environ.get("MONGO_db_url")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.labtrack
equipment_collection = database.equipment

# Pydantic models for request validation and response serialization
class Equipment(BaseModel):
    name: str
    count: int
    type: str
    danger_factor: int
    expiry_date: Optional[str]
    lab: str  # New field for lab information
    shelf_number: str  # New field for shelf number

class UpdateEquipment(BaseModel):
    name: Optional[str]
    count: Optional[int]
    type: Optional[str]
    danger_factor: Optional[int]
    expiry_date: Optional[str]
    lab: Optional[str]  # New field for lab information
    shelf_number: Optional[str]  # New field for shelf number

class EquipmentResponse(Equipment):
    id: str  # ID of the equipment in the response

# Helper function to format equipment documents for responses
# Converts MongoDB document to a dictionary with a string representation of the ObjectId
def equipment_helper(equipment) -> dict:
    return {
        "id": str(equipment["_id"]),
        "name": equipment["name"],
        "count": equipment["count"],
        "type": equipment["type"],
        "danger_factor": equipment["danger_factor"],
        "expiry_date": equipment["expiry_date"],
        "lab": equipment["lab"],  # New field for lab information
        "shelf_number": equipment["shelf_number"]  # New field for shelf number
    }

# Route to list all equipment with optional query parameters
# You can filter equipment by any of the provided query parameters.
# If no parameters are provided, all equipment will be listed.
@app.get("/equipments", response_description="List all equipment", response_model=List[EquipmentResponse])
async def get_equipments(
    id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    count: Optional[int] = Query(None),
    type: Optional[str] = Query(None),
    danger_factor: Optional[int] = Query(None),
    expiry_date: Optional[str] = Query(None),
    lab: Optional[str] = Query(None),
    shelf_number: Optional[str] = Query(None)
):
    query = {}
    if id:
        try:
            query["_id"] = ObjectId(id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID format")
    if name:
        query["name"] = name
    if count:
        query["count"] = count
    if type:
        query["type"] = type
    if danger_factor:
        query["danger_factor"] = danger_factor
    if expiry_date:
        query["expiry_date"] = expiry_date
    if lab:
        query["lab"] = lab
    if shelf_number:
        query["shelf_number"] = shelf_number

    equipments = []
    async for equipment in equipment_collection.find(query):
        equipments.append(equipment_helper(equipment))
    return equipments

# Route to add new equipment
# Requires an Equipment object in the request body. The equipment is added to the database.
# Returns the newly created equipment, including its MongoDB ID.
@app.post("/equipment", response_description="Add new equipment", response_model=EquipmentResponse)
async def new_equipment(equipment: Equipment):
    equipment = equipment.dict()
    result = await equipment_collection.insert_one(equipment)
    new_equipment = await equipment_collection.find_one({"_id": result.inserted_id})
    return equipment_helper(new_equipment)

# Route to delete an equipment by ID
# The ID must be provided as a URL path parameter. If the equipment is found and deleted, a success message is returned.
# If no equipment is found with the provided ID, a 404 error is returned.
@app.delete("/equipment/{id}", response_description="Delete an equipment")
async def delete_equipment(id: str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await equipment_collection.delete_one({"_id": object_id})
    if result.deleted_count == 1:
        return {"message": "Equipment deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Equipment with ID {id} not found")

# Route to update an equipment by ID
# Requires an ID as a URL path parameter and an UpdateEquipment object in the request body.
# Only fields provided in the UpdateEquipment object will be updated.
# Returns the updated equipment if successful, or a 404 error if no equipment is found with the provided ID.
@app.put("/equipment/{id}", response_description="Update an equipment", response_model=EquipmentResponse)
async def update_equipment(id: str, equipment: UpdateEquipment):
    update_data = {k: v for k, v in equipment.dict().items() if v is not None}
    result = await equipment_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 1:
        updated_equipment = await equipment_collection.find_one({"_id": ObjectId(id)})
        return equipment_helper(updated_equipment)
    raise HTTPException(status_code=404, detail=f"Equipment with ID {id} not found")

# Route to add multiple equipment items in bulk
# Requires a list of Equipment objects in the request body. All equipment items are added to the database in one operation.
# Returns the list of newly created equipment items, including their MongoDB IDs.
@app.post("/bulk_add", response_description="Add multiple equipment", response_model=List[EquipmentResponse])
async def bulk_add(equipments: List[Equipment]):
    equipment_list = [equipment.dict() for equipment in equipments]
    result = await equipment_collection.insert_many(equipment_list)
    new_equipments = await equipment_collection.find({"_id": {"$in": result.inserted_ids}}).to_list(length=len(result.inserted_ids))
    return [equipment_helper(equipment) for equipment in new_equipments]

# Route to delete multiple equipment items by their IDs
# Requires a list of equipment IDs in the request body. All specified equipment items are deleted in one operation.
# Returns a message indicating the number of deleted items, or a 404 error if no equipment is found with the provided IDs.
@app.delete("/bulk_remove", response_description="Delete multiple equipment")
async def bulk_remove(ids: List[str]):
    object_ids = [ObjectId(id) for id in ids]
    result = await equipment_collection.delete_many({"_id": {"$in": object_ids}})
    if result.deleted_count > 0:
        return {"message": f"{result.deleted_count} equipment(s) deleted successfully"}
    raise HTTPException(status_code=404, detail="No equipment found with the provided IDs")

# Ping Command
@app.get("/")
async def ping():
    return "pong"

# Run the FastAPI app with uvicorn
# This script runs the app in development mode with auto-reloading enabled. For production, you should use a production-grade ASGI server.
if __name__ == "__main__":
    import uvicorn

    # Get port number from environment variable PORT, defaulting to 8000 if not set
    port = int(os.getenv("PORT", 8000))
    
    # Run the FastAPI application using Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
