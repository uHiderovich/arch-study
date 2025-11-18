from fastapi import APIRouter, Depends
from .dependencies import fake_users_db
from .products import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_me(user = Depends(get_current_user)):
    return user
