import os

from redis import Redis


def get_redis_connection():
    r = Redis(
        host=os.environ['REDIS_HOST'],
        port=42687,
        password=os.environ['REDIS_PASSWORD'],
        ssl=True
    )

    return r


# Dependency FastAPI
def get_redis():
    r = get_redis_connection()

    try:
        yield r
    finally:
        r.close()
