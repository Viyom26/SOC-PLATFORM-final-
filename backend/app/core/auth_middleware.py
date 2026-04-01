from fastapi import Request, HTTPException
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

# 🔐 LOAD ENV
load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY") or ""

async def verify_jwt(request: Request):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(
            token.split(" ")[1],
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")