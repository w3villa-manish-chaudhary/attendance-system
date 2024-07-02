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
        
        # Retrieve the user details before deleting
        user = users_collection.find_one({"_id": user_object_id})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        
        result = users_collection.delete_one({"_id": user_object_id})
        
        if result.deleted_count == 1:
            
            user_folder = os.path.join("known_faces", user['username'])
            if os.path.exists(user_folder):
                for filename in os.listdir(user_folder):
                    file_path = os.path.join(user_folder, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        raise HTTPException(status_code=500, detail=f"Error deleting file {file_path}: {str(e)}")
                os.rmdir(user_folder)
            
            return {"message": "User and images deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))