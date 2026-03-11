from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
import uuid
import re
import bcrypt

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audit_log import AuditLog
from app.models.user import User

# ================= CONFIG =================

SECRET_KEY = "SOC_PLATFORM_SUPER_SECRET_KEY_2026_CHANGE_ME_NOW"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ================= PASSWORD VALIDATION =================

def validate_password(password: str):

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"

    if not re.match(pattern, password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters including uppercase, lowercase, number and special symbol"
        )

# ================= DEV USERS (LEGACY SUPPORT) =================

USERS = {
    "admin@example.com": {
        "username": "admin@example.com",
        "password": "Admin@123",
        "role": "ADMIN"
    },
    "analyst@example.com": {
        "username": "analyst@example.com",
        "password": "Analyst@123",
        "role": "ANALYST"
    }
}

# =====================================================
# REGISTER NEW USER (DATABASE)
# =====================================================

def register_user(email: str, password: str, db: Session):

    validate_password(password)

    existing = db.query(User).filter(User.email == email).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(
        id=str(uuid.uuid4()),
        email=email,
        hashed_password=hashed,
        role="ADMIN"
    )

    db.add(user)
    db.commit()

    return {"message": "User created successfully"}

# =====================================================
# LOGIN USER (DATABASE + LEGACY USERS)
# =====================================================

def login_user(username: str, password: str, db: Session):

    validate_password(password)

    # -----------------------------
    # FIRST CHECK DATABASE USERS
    # -----------------------------

    user = db.query(User).filter(User.email == username).first()

    if user:

        if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        role = user.role

    else:

        # -----------------------------
        # FALLBACK TO LEGACY USERS
        # -----------------------------

        legacy_user = USERS.get(username)

        if not legacy_user or legacy_user["password"] != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        role = legacy_user["role"]

    # -----------------------------
    # CREATE TOKEN
    # -----------------------------

    token = jwt.encode(
        {
            "sub": username,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=8),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    # -----------------------------
    # AUDIT LOG
    # -----------------------------

    try:

        db.add(
            AuditLog(
                id=str(uuid.uuid4()),
                user=username,
                action="LOGIN",
                target=username,
                page="login",
                severity="INFO",
                created_at=datetime.utcnow(),
            )
        )

        db.commit()

    except Exception:
        db.rollback()

    return {"access_token": token, "token_type": "bearer"}

# ================= AUTH =================

def get_current_user(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload

    except jwt.ExpiredSignatureError:

        raise HTTPException(status_code=401, detail="Token expired")

    except Exception:

        raise HTTPException(status_code=401, detail="Not authenticated")


def require_role(*roles):

    def checker(user=Depends(get_current_user)):

        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user

    return checker