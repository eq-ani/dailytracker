from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

# Import models and database
from app.models.habit import Habit
from app.database import SessionLocal
from app.schemas.habit import HabitCreate, HabitResponse
from app.auth.jwt import verify_token  # New import

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")  # New

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# New dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit: HabitCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # New dependency
):
    """
    Create a new habit (now protected by JWT)
    """
    existing_habit = db.query(Habit).filter(Habit.name == habit.name).first()
    if existing_habit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Habit with this name already exists"
        )
    
    db_habit = Habit(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.get("/habits/", response_model=List[HabitResponse])
def list_habits(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # New dependency
):
    """
    Retrieve all habits (now protected by JWT)
    """
    return db.query(Habit).all()