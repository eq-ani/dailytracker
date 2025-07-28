from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import models and database
from app.models.habit import Habit
from app.database import SessionLocal
from app.schemas.habit import HabitCreate, HabitResponse  # New imports

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    """
    Create a new habit with validation.
    
    Example request body:
    {
        "name": "Exercise",
        "frequency": "daily"
    }
    """
    # Check if habit already exists
    existing_habit = db.query(Habit).filter(Habit.name == habit.name).first()
    if existing_habit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Habit with this name already exists"
        )
    
    db_habit = Habit(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)  # Populates generated fields like ID
    return db_habit

@router.get("/habits/", response_model=List[HabitResponse])
def list_habits(db: Session = Depends(get_db)):
    """
    Retrieve all habits with their full details.
    Returns list of habits with ids, names, and frequencies.
    """
    return db.query(Habit).all()