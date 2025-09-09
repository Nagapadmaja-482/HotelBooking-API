from bson import ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from typing import Any

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            function=cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v), when_used="always"
            )
        )
    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError(f"Invalid ObjectId: {v}")

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string","example":"650c7ab7e6e45f07cc3b203c"}
    

from beanie import Document
from typing import List, Annotated,Optional
from pydantic import Field, ConfigDict


class Hotel(Document):
    name: str
    location: str
    description: str
    ratings: float = 0.0
    amenities: List[str]
    price_per_night: float
    owner_id: PyObjectId= Field(...)
    id: Optional[PyObjectId] = Field(alias="_id")

    model_config = {
        "arbitrary_types_allowed":True,
        "populate_by_name":True,
    }

    class Settings:
        name = "hotels"

from pydantic import BaseModel
from typing import List

class HotelIn(BaseModel):
    name: str
    location: str
    description: str
    ratings: float
    amenities: List[str]
    price_per_night: float


