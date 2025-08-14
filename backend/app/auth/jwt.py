from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from typing import Optional

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY") or "your-secret-key-here"  # Fallback for dev
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY.encode(), algorithm=ALGORITHM)  # Added .encode()

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY.encode(),  # Added .encode()
            algorithms=[ALGORITHM],
            options={"verify_aud": False}
        )
        return payload.get("sub")
    except JWTError:
        return None