from fastapi import FastAPI
from app.database import init_db
from app.routes import user, hotel, booking , room

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to StayMate API"}


app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(hotel.router, prefix="/api/hotels", tags=["Hotels"])
app.include_router(booking.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(room.router, prefix="/api/rooms", tags=["Rooms"])

