from redis import Redis

redis_client = None

def get_redis_connection():
    global redis_client
    try:
        redis_client = Redis(host='localhost', port=6379, db=0)
        return redis_client
    except Exception as e:
        raise Exception(f"Error connecting to Redis: {str(e)}")

def clear_redis():
    try:
        redis_client.flushdb()
        print("Redis database cleared.")
    except Exception as e:
        raise Exception(f"Error clearing Redis database: {str(e)}")

# Example usage:
if __name__ == "__main__":
    get_redis_connection()
    clear_redis()
