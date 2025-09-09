from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "u4oG_BH96oJxT8JZZgkfNq9Or2sH6XmB2vQpXymIv4z-s3n_1K0eUeD2oXz3g1Rg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360

def create_access_token(data: dict)->str:
    email = data.get("email")
    print("Creating token for:", email)  # 👈 Add this

    if not email or not isinstance(email, str):
        raise ValueError("Invalid or missing 'email' for JWT subject")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "sub": email})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str)-> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Valid token. Payload:", payload)
        return payload
    except JWTError as e:
        print("Token verification failed:", e)
        return None
