from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://habit_user:habit_pass@localhost/habit_tracker"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This must be imported AFTER declarative_base()
Base = declarative_base()

# Import all models HERE to ensure they're registered
from app.models.user import User  # noqa: F401
from app.models.habit import Habit  # noqa: F401