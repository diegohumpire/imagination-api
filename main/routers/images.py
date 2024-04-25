from typing import Annotated, Generic, TypeVar

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel


from main.routers.filters import check_session
from main.services.ia import generate_image

T = TypeVar("T")

router = APIRouter(tags=["Images"])


class InputPromptImage(BaseModel):
    prompt: str


class ResultData(BaseModel, Generic[T]):
    type: str
    data: T


class ImageData(BaseModel):
    url: str
    sizeString: str
    size: dict


class ImageResponse(ResultData[ImageData]):
    type: str = "image"


class PromptResult(BaseModel, Generic[T]):
    inputPrompt: str
    result: T


@router.post("/images", status_code=status.HTTP_201_CREATED, response_model=PromptResult[ResultData])
async def create_image(input: InputPromptImage, session_uuid: Annotated[check_session, Depends()]):
    url = generate_image(input.prompt, session_uuid)

    image_data = ImageResponse(data=ImageData(
        url=url, sizeString="512x512", size={"width": 512, "height": 512}))

    return PromptResult(inputPrompt=input.prompt, result=image_data)
