from fastapi import APIRouter, Depends, HTTPException
from jose import jwt as jose_jwt, JWTError
from fastapi import Header
from .dependencies import fake_products, fake_users_db
from .auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/products", tags=["products"])


def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return fake_users_db.get(username)
    except JWTError:
        raise HTTPException(401, "Invalid token")


@router.get("/")
def get_products(user=Depends(get_current_user)):
    return fake_products
