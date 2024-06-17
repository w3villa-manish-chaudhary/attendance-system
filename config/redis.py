from redis import Redis

redis_client = None

def get_redis_connection():
    global redis_client
    try:
        redis_client = Redis(host='localhost', port=6379, db=0)
        return redis_client
    except Exception as e:
        raise Exception(f"Error connecting to Redis: {str(e)}")
