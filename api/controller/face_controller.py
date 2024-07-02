from fastapi import HTTPException
from api.models.face_model import ImageData
from config.db import connect_to_mongo
from api.services.face_service import process_images
from api.handlers.helper import serialize_face
import base64
from bson import ObjectId
import os

async def register_faces(data: ImageData):
    try:
        response = await process_images(data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        return None

async def known_faces():
    try:
        client = connect_to_mongo()
        db = client['attendance']
        users_collection = db['known_faces']
        faces = users_collection.find()
        
        serialized_faces = []
        for face in faces:
            user = serialize_face(face)
            user_images = []
            for image in user['images']:
                image_path = os.path.join('known_faces', user['username'], image)
                encoded_image = encode_image(image_path)
                user_images.append({
                    "filename": image,
                    "data": encoded_image
                })
            user['images'] = user_images
            serialized_faces.append(user)
        
        return serialized_faces
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def delete_user_from_db(user_id: str):
    try:
        client = connect_to_mongo()
        db = client['attendance']
        users_collection = db['known_faces']

        user_object_id = ObjectId(user_id)
        
        result = users_collection.delete_one({"_id": user_object_id})
        
        if result.deleted_count == 1:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

