from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # For frontend connection later
from app.routers import habits
from app.database import engine
from app.models import habit
from app.auth import router as auth_router

# Create all database tables (optional safety net - Alembic should handle this)
habit.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Habit Tracker API",
    description="Backend for tracking daily habits",
    version="0.1.0"
)

# Add CORS middleware (enable when frontend is ready)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(habits.router, prefix="/api")

# Health check endpoint
@app.get("/")
def home():
    return {"status": "API is running"}

def print_routes():
    for route in app.routes:
        print(f"{route.path} -> {route.methods}")

print_routes()