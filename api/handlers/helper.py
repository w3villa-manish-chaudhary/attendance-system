import cv2
import numpy as np
import os
from config.redis import get_redis_connection
import face_recognition

def save_image(img_path, img):
    try:
        print("Here ==============================>")
        cv2.imwrite(img_path, img)
        print("Saved successfully!")
    except Exception as e:
        raise Exception(f"Error saving image: {str(e)}")


def load_face_encodings(users_collection):
  try:
    users = users_collection.find({})
    face_encodings = []
    for user in users:
        for encoding in user['encodings']:
            face_encodings.append(np.frombuffer(encoding, dtype=np.float64)) 
    return face_encodings
  except Exception as e:
        raise Exception(f"Error in finding encodings: {str(e)}")
      
# Utility to get encodings from Redis
def get_encodings():
    redis_client = get_redis_connection()
    keys = redis_client.keys('*_faces')  # Adjusted to match the key pattern used for storing
    known_face_encodings = []
    known_face_names = []

    for key in keys:
        name = key.decode('utf-8').replace('_faces', '')  # Adjust to strip the correct suffix
        stored_encodings = redis_client.hgetall(key)

        for field_name, encoding_bytes in stored_encodings.items():
            encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
            known_face_encodings.append(encoding)
            known_face_names.append(name)

    redis_client.close()  # Close the connection after use
    return known_face_encodings, known_face_names
  
# Save faces and encodings in Redis
def save_face_and_encodings(name, frame, face_encoding, count):
    redis_client = get_redis_connection()
    user_folder = f'unknown_faces/{name}'
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    image_path = os.path.join(user_folder, f'{name}_{count}.jpg')
    cv2.imwrite(image_path, frame)
    print(f'Image saved as {image_path}')

    encoding_key = f'{name}_faces'
    field_name = f'encoding_{count}'
    redis_client.hset(encoding_key, field_name, face_encoding.tobytes())
    print(f'Encoding saved in Redis hash with key {encoding_key} and field {field_name}')


def serialize_face(face):
    base_server_url = "http://localhost:8000"
    return {
        "id": str(face["_id"]),
        "username": face.get("username", "N/A"), 
        "images": face.get("images", []), 
        # "image_path": f"{base_server_url}/{face.get('image_path', 'default.jpg')}", 
    }
    
# Load known faces
def load_known_faces(base_directory="known_faces"):
    known_faces = []
    known_names = []
    # Walk through the directory tree
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".jpg"):  # Assumes all images are JPEGs
                path = os.path.join(root, file)
                image = face_recognition.load_image_file(path)
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    encoding = face_encodings[0]
                    known_faces.append(encoding)
                    # Assuming the subfolder's name is the person's name
                    known_names.append(os.path.basename(root))
    return known_faces, known_names

def load_unknown_faces(base_directory="unknown_faces"):
    unknown_faces = []
    unknown_identifiers = []

    # Ensure the directory exists
    if not os.path.exists(base_directory):
        print("Directory not found:", base_directory)
        return unknown_faces, unknown_identifiers

    # Walk through the directory tree
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.lower().endswith(".jpg"):  # Assumes all images are JPEGs
                path = os.path.join(root, file)
                image = face_recognition.load_image_file(path)
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    # Typically, there should be one face per image in this scenario
                    encoding = face_encodings[0]
                    unknown_faces.append(encoding)
                    unknown_identifiers.append(os.path.splitext(file)[0])  # Save the identifier without the file extension

    return unknown_faces, unknown_identifiers
