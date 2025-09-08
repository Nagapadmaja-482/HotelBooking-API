# app/routes/room.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.room import Room
from app.auth.auth import get_current_user
from app.models.user import User
from bson import ObjectId

router = APIRouter()

# Create room (Hotelier only)
@router.post("/")
async def create_room(room: Room, user: User = Depends(get_current_user)):
    if user.role != "hotelier":
        raise HTTPException(status_code=403, detail="Only hoteliers can add rooms")
    await room.insert()
    return {"message": "Room created", "room_id": str(room.id)}

# List all rooms
@router.get("/", response_model=List[Room])
async def list_rooms():
    return await Room.find_all().to_list()

# Get room by ID
@router.get("/{room_id}")
async def get_room(room_id: str):
    room = await Room.get(ObjectId(room_id))
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# Update room (Hotelier only)
@router.put("/{room_id}")
async def update_room(room_id: str, updated_room: Room, user: User = Depends(get_current_user)):
    if user.role != "hotelier":
        raise HTTPException(status_code=403, detail="Not authorized")
    room = await Room.get(ObjectId(room_id))
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.room_type = updated_room.room_type
    room.price = updated_room.price
    room.available_count = updated_room.available_count
    await room.save()
    return {"message": "Room updated"}

# Delete room (Hotelier only)
@router.delete("/{room_id}")
async def delete_room(room_id: str, user: User = Depends(get_current_user)):
    if user.role != "hotelier":
        raise HTTPException(status_code=403, detail="Not authorized")
    room = await Room.get(ObjectId(room_id))
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    await room.delete()
    return {"message": "Room deleted"}
