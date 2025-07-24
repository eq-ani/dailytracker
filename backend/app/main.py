from fastapi import FastAPI # type: ignore

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/habits")
def list_habits():
    return {"habits": ["Drink water", "Exercise"]}