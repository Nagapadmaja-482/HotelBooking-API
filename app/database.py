
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.hotel import Hotel
from app.models.user import User
from app.models.room import Room
from app.models.booking import Booking

async def init_db():
    MONGODB_URI = "mongodb+srv://NagaPadmaja:Paddu456@cluster0.xkoqkll.mongodb.net/"
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.hotelbooking_db

    await init_beanie(
        database=db,
        document_models=[User, Hotel, Room, Booking]
    )
