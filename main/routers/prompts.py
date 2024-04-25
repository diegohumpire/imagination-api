
from typing import Annotated, Generic, TypeVar

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from main.routers.filters import check_session
from main.services.ia import generate_prompts

T = TypeVar("T")

router = APIRouter(tags=["Prompts"])


class ListResponse(BaseModel, Generic[T]):
    data: list[T]


class PromptItem(BaseModel):
    text: str
    title: str


@router.get(
    "/prompts",
    status_code=status.HTTP_200_OK,
    response_model=ListResponse[PromptItem],
    dependencies=[Depends(check_session)])
async def get_prompts(session_uuid: Annotated[check_session, Depends()]):
    prompts = generate_prompts(session_uuid)

    return {
        "data": prompts
    }
