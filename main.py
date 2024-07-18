from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# FastAPI instance
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware configuration 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, modify this based on your requirements
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# MongoDB configuration
MONGO_DETAILS = "mongo_db_url"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.labtrack
equipment_collection = database.equipment

# Pydantic models
class Equipment(BaseModel):
    name: str
    count: int
    type: str
    danger_factor: int
    expiry_date: Optional[str]  # Now it's a simple string

class UpdateEquipment(BaseModel):
    name: Optional[str]
    count: Optional[int]
    type: Optional[str]
    danger_factor: Optional[int]
    expiry_date: Optional[str]  # Now it's a simple string

class EquipmentResponse(Equipment):
    id: str

# Utility functions
def equipment_helper(equipment) -> dict:
    return {
        "id": str(equipment["_id"]),
        "name": equipment["name"],
        "count": equipment["count"],
        "type": equipment["type"],
        "danger_factor": equipment["danger_factor"],
        "expiry_date": equipment["expiry_date"]
    }

# Routes
@app.get("/equipments", response_description="List all equipment", response_model=List[EquipmentResponse])
async def get_equipments():
    equipments = []
    async for equipment in equipment_collection.find():
        equipments.append(equipment_helper(equipment))
    return equipments

@app.post("/equipment", response_description="Add new equipment", response_model=EquipmentResponse)
async def new_equipment(equipment: Equipment):
    equipment = equipment.dict()
    result = await equipment_collection.insert_one(equipment)
    new_equipment = await equipment_collection.find_one({"_id": result.inserted_id})
    return equipment_helper(new_equipment)

@app.delete("/equipment/{id}", response_description="Delete an equipment")
async def delete_equipment(id: str):
    result = await equipment_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Equipment deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Equipment with ID {id} not found")

@app.put("/equipment/{id}", response_description="Update an equipment", response_model=EquipmentResponse)
async def update_equipment(id: str, equipment: UpdateEquipment):
    update_data = {k: v for k, v in equipment.dict().items() if v is not None}
    result = await equipment_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 1:
        updated_equipment = await equipment_collection.find_one({"_id": ObjectId(id)})
        return equipment_helper(updated_equipment)
    raise HTTPException(status_code=404, detail=f"Equipment with ID {id} not found")

@app.post("/bulk_add", response_description="Add multiple equipment", response_model=List[EquipmentResponse])
async def bulk_add(equipments: List[Equipment]):
    equipment_list = [equipment.dict() for equipment in equipments]
    result = await equipment_collection.insert_many(equipment_list)
    new_equipments = await equipment_collection.find({"_id": {"$in": result.inserted_ids}}).to_list(length=len(result.inserted_ids))
    return [equipment_helper(equipment) for equipment in new_equipments]

@app.delete("/bulk_remove", response_description="Delete multiple equipment")
async def bulk_remove(ids: List[str]):
    object_ids = [ObjectId(id) for id in ids]
    result = await equipment_collection.delete_many({"_id": {"$in": object_ids}})
    if result.deleted_count > 0:
        return {"message": f"{result.deleted_count} equipment(s) deleted successfully"}
    raise HTTPException(status_code=404, detail="No equipment found with the provided IDs")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)