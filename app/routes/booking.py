from fastapi import APIRouter, Depends, HTTPException
from app.models.booking import Booking
from app.models.room import Room
from app.auth.auth import get_current_user
from datetime import date
from app.models.user import User
from app.models.room import Room
from pydantic import BaseModel
from app.models.booking import Booking

class BookingRequest(BaseModel):
    room_id: str
    check_in: date
    check_out: date


router = APIRouter()

@router.post("/",response_model = dict)
async def book_room(
    booking_req: BookingRequest,
    user: User = Depends(get_current_user)

):
    room = await Room.get(booking_req.room_id)
    if not room or room.available_count <= 0:
        raise HTTPException(status_code=400, detail="Room not available")

    booking = Booking(
        user_id=user.id,
        room_id=room.id,
        check_in=booking_req.check_in,
        check_out=booking_req.check_out
    )
    await booking.insert()

    room.available_count -= 1
    await room.save()

    return {"message": "Booking successful", "booking_id": str(booking.id)}
