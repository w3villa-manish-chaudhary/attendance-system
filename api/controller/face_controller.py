from fastapi import HTTPException
from api.models.face_model import ImageData
from config.db import connect_to_mongo
from api.services.face_service import process_images
from api.handlers.helper import serialize_face 

async def register_faces(data: ImageData):
    try:
        response = await process_images(data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def known_faces():
    try:
        client = connect_to_mongo()
        db = client['face_recognition']
        users_collection = db['users']
        faces = users_collection.find()
        serialized_faces = [serialize_face(face) for face in faces]
        return serialized_faces
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))