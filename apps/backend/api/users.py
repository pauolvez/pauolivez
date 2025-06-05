from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .deps import get_db, get_current_superuser
from ..models.user import User
from .auth import get_password_hash

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    is_superuser: bool = False

@router.post("/users", response_model=dict)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), _=Depends(get_current_superuser)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_superuser=user_in.is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}
