from pydantic import BaseModel
from typing import Optional

class HabitBase(BaseModel):
    name: str
    frequency: Optional[str] = "daily"

class HabitCreate(HabitBase):
    pass

class HabitResponse(HabitBase):
    id: int
    
    class Config:
        orm_mode = True  # Allows conversion from SQLAlchemy model