from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal_users
from models import User
from schema import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


def get_db_users():
    db = SessionLocal_users()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(payload: UserCreate, db: Session = Depends(get_db_users)):
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        return {"message": "Username already exists"}

    new_user = User(username=payload.username)
    new_user.set_password(payload.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(payload: UserCreate, db: Session = Depends(get_db_users)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not user.check_password(payload.password):
        return {"message": "Login failure"}

    return {"message": "Successfully logged in"}
