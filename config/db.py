from pymongo import MongoClient

mongo_client = None

def connect_to_mongo():
    global mongo_client
    try:
        mongo_client = MongoClient('mongodb://localhost:27017/')
        return mongo_client
    except Exception as e:
        raise Exception(f"Error connecting to MongoDB: {str(e)}")
