from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.controller.face_controller import register_faces, known_faces
from api.models.face_model import ImageData
from api.services.face_service import generate_frames

router = APIRouter()

@router.post("/register")
async def register_faces_endpoint(data: ImageData):
    return await register_faces(data)

@router.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get('/get_faces')
async def get_faces():
    return await known_faces()


