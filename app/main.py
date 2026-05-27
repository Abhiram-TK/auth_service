from fastapi import FastAPI
from app.database import engine

app = FastAPI()

@app.get("/")
def test_connection():
    return {"message": "Database connection setup successful"}