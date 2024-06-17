from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.face_routes import router as face_router
from config.db import connect_to_mongo
from config.redis import get_redis_connection
import os

app = FastAPI()

os.makedirs('known_faces', exist_ok=True)
os.makedirs('unknown_faces', exist_ok=True)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5001", 'http://127.0.0.1:5000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(face_router)

@app.on_event("startup")
def startup_db_client():
    connect_to_mongo()
    get_redis_connection()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Face Recognition API"}
