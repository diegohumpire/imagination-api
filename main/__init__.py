import os
import uuid
from typing import TypeVar, Generic

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, EmailStr
from redis import Redis

from main.prompts import generate_prompts, generate_image

T = TypeVar("T")

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


@app.post("/session", status_code=status.HTTP_201_CREATED)
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


class ListResponse(BaseModel, Generic[T]):
    data: list[T]


class PromptItem(BaseModel):
    text: str
    title: str


@app.get("/prompts", status_code=status.HTTP_200_OK, response_model=ListResponse[PromptItem])
async def get_prompts(redis: Redis = Depends(get_redis)):
    prompts = generate_prompts()
    return {
        "data": prompts
    }


class PromptImage(BaseModel):
    prompt: str


@app.post("/images", status_code=status.HTTP_201_CREATED)
async def create_image(input: PromptImage, redis: Redis = Depends(get_redis)):
    url = generate_image(input.prompt)

    return {
        "image_url": url,
    }
