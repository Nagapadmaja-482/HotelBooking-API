from fastapi import APIRouter, Depends
from typing import List
from app.models.hotel import Hotel
from app.auth.auth import get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_hotel(hotel: Hotel, user=Depends(get_current_user)):
    hotel.owner_id = ObjectId(user.id)
    await hotel.insert()
    return hotel

@router.get("/", response_model=List[Hotel])
async def list_hotels():
    return await Hotel.find_all().to_list()
