from beanie import Document
from bson import ObjectId
from pydantic import Field, ConfigDict


#class Room(Document):
    #id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    #hotel_id: ObjectId
    #room_type: str
    #price: float
    #available_count: int
    #model_config = ConfigDict(arbitrary_types_allowed=True)

class Room(Document):
    hotel_id: ObjectId = Field(...)
    room_type: str
    price: float
    available_count: int

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "rooms"
