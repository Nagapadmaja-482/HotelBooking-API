from beanie import Document
from pydantic import EmailStr
from enum import Enum
from pydantic import Field, ConfigDict
from bson import ObjectId
from typing import Optional


class Role(str, Enum):
    guest = "guest"
    hotelier = "hotelier"

class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: str
    role: Role
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    class Settings:
        name = "users"
