# Code below created with the help of this tutorial: https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/

import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://shelby:shelbytest@cluster0.3zfyo65.mongodb.net/test")
db = client.sample_geospatial

app = FastAPI()

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Define model
# Set default value as None to avoid triggering error when there is no value for that field in MongoDB
class ShipwreckModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    rcrd: Optional[str] = None
    vesslterms: Optional[str] = None
    feature_type: Optional[str] = None
    chart: Optional[str] = None
    latdec: Optional[float] = None
    londec: Optional[float] = None
    gp_quality: Optional[str] = None
    depth: Optional[float] = None
    sounding_type: Optional[str] = None
    quasou: Optional[str] = None
    watlev: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "_id": {
                "$oid": "578f6fa2df35c7fbdbaed8ec"
            },
            "recrd": "",
            "vesslterms": "",
            "feature_type": "Wrecks - Visible",
            "chart": "US,US,reprt,L-1453/14",
            "latdec": 18.5640431,
            "londec": -72.3525848,
            "gp_quality": "",
            "depth": 0,
            "sounding_type": "",
            "history": "",
            "quasou": "",
            "watlev": "always dry",
        }

# Get all shipwrecks
@app.get(
    "/", response_description="List all shipwreckss", response_model=List[ShipwreckModel]
)
async def list_shipwrecks():
    shipwrecks = await db["shipwrecks"].find().to_list(1000)
    return shipwrecks

if __name__ == '__main__':
    uvicorn.run(app)