import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import habits
from app.database import engine
from app.models import habit
from app.auth import router as auth_router
from dotenv import load_dotenv

# Simplified env loading
load_dotenv()  # Now looks for .env in root automatically

app = FastAPI(
    title="Habit Tracker API",
    description="Backend for tracking daily habits",
    version="0.1.0"
)

# Database setup
habit.Base.metadata.create_all(bind=engine)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(habits.router, prefix="/api")

@app.get("/")
def home():
    return {"status": "API is running"}