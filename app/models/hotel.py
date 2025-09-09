from bson import ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return cls(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string"}
from beanie import Document
from typing import List, Annotated
from pydantic import Field, ConfigDict


class Hotel(Document):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    name: str
    location: str
    description: str
    ratings: float = 0.0
    amenities: List[str]
    price_per_night: float
    owner_id: Annotated[PyObjectId, Field(...)]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}  # Optional, for JSON output
    )

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


