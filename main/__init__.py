import os
import uuid

from fastapi import Depends, FastAPI
from pydantic import BaseModel, EmailStr
from redis import Redis

app = FastAPI()


# Dependency
def get_redis():
    r = Redis(
        host=os.environ['REDIS_HOST'],
        port=42687,
        password=os.environ['REDIS_PASSWORD'],
        ssl=True
    )

    try:
        yield r
    finally:
        r.close()


class SessionInput(BaseModel):
    email: EmailStr


@app.post("/session")
async def crate_session(input: SessionInput, redis: Redis = Depends(get_redis)):
    uuid_ = str(uuid.uuid4())
    redis.set(input.email, uuid_, ex=3600)

    if redis.exists(input.email):
        return {
            "session": redis.get(input.email),
        }

    return {
        "session": uuid_,
    }


@app.get("/hello/{name}")
async def get_name(name: str):
    return {
        "name": name,
    }


@app.get("/bye/{name}")
async def say_bye(name: str):
    return {
        "name": name,
    }
