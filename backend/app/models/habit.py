from app.database import Base
from sqlalchemy import Column, Integer, String

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)  # e.g., "Drink water"
    frequency = Column(String(20), default="daily")  # "daily" or "weekly"