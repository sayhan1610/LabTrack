from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# FastAPI instance
app = FastAPI()

# MongoDB configuration
MONGO_DETAILS = "mongo_url"

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




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)