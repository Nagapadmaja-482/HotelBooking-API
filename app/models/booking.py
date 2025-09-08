from beanie import Document
from bson import ObjectId
from datetime import date
from pydantic import Field, ConfigDict


class Booking(Document):
    user_id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    room_id: ObjectId
    check_in: date
    check_out: date
    status: str = "confirmed"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    class Settings:
        name = "bookings"
