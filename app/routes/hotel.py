from fastapi import APIRouter, Depends
from typing import List
from app.models.hotel import Hotel,HotelIn,PyObjectId
from app.auth.auth import get_current_user
from bson import ObjectId


router = APIRouter()

@router.post("/")
async def create_hotel(hotel_data: HotelIn, user=Depends(get_current_user)):
    hotel = Hotel(
        **hotel_data.dict(),
        owner_id=(str(user.id))  # ✅ this works with the fixed model
    )
    await hotel.insert()
    return hotel

@router.get("/", response_model=List[Hotel])
async def list_hotels():
    return await Hotel.find_all().to_list()
