from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.models.user import User, Role
from app.auth.auth import hash_password, verify_password
from app.auth.jwt import create_access_token

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Role

@router.post("/register")
async def register(user_data: UserCreate):
    existing = await User.find_one(User.email == user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )
    await user.insert()
    return {"message": "User registered"}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(user_data: UserLogin):
    user = await User.find_one(User.email == user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer","payload": {"sub": user.email}}
