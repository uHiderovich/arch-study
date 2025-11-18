import bcrypt
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from jose import jwt as jose_jwt
from .dependencies import fake_users_db
from .models import UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "a-string-secret-at-least-256-bits-long"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed.encode("utf-8"),
    )


def create_access_token(data: dict, expires_minutes=30):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jose_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(body: UserLogin):
    user = fake_users_db.get(body.username)
    if not user:
        raise HTTPException(401, "User not found")

    if not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(401, "Wrong password")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(body: UserRegister):
    username = body.username.lower()

    if username in fake_users_db:
        raise HTTPException(400, "User already exists")

    hashed = hash_password(body.password)

    new_user = {
        "id": len(fake_users_db) + 1,
        "username": username,
        "email": body.email,
        "hashed_password": hashed
    }

    fake_users_db[username] = new_user

    return {"message": "User registered", "user": new_user}
