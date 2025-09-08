from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.auth.jwt import verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("Token received:", token)
    payload = verify_token(token)
    if payload is None:
        print("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")
    print("Payload decoded:", payload)
    user = await User.find_one(User.email == payload["sub"])
    if user is None:
        print("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user
