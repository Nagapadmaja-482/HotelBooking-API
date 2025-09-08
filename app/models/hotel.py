from beanie import Document
from pydantic import Field, ConfigDict,BaseModel
from typing import List
from bson import ObjectId

class Hotel(Document):
    name: str
    location: str
    description: str
    amenities: List[str]
    rating: float = 0.0
    price_per_night: float
    #owner_id: ObjectId = Field(default_factory=ObjectId, alias="_id")

    #model_config = ConfigDict(arbitrary_types_allowed=True)

    class Settings:
        name = "hotels"