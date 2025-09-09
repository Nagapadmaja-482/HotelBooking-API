from bson import ObjectId
from pydantic_core import core_schema
from typing import Any
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic import BaseModel
from typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        def validate(v: Any,) -> ObjectId:
            if isinstance(v, ObjectId):
                return v
            if isinstance(v, str) and ObjectId.is_valid(v):
                return ObjectId(v)
            raise ValueError(f"Invalid ObjectId: {v}")

        # ✅ Only pass the validator function
        return core_schema.no_info_plain_validator_function(
            validate,
             serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v), when_used="always"
            )
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler:GetJsonSchemaHandler ) -> JsonSchemaValue:
        return {"type": "string", "example": "650c7ab7e6e45f07cc3b203c"}


from beanie import Document
from bson import ObjectId


class Room(Document):
    hotel_id:PyObjectId
    hotel_name:str
    room_number:str
    room_type: str
    price: float
    available_count: int
    is_available:bool
    model_config = {
    "arbitrary_types_allowed": True}

    class Settings:
        name = "rooms"
class RoomUpdate(BaseModel):
    room_type: Optional[str] = None
    price: Optional[float] = None
    available_count: Optional[int] = None
