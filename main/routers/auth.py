from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr

from main.services.sessions import create_session_from_email

router = APIRouter(tags=["Authentication"])


class SessionInput(BaseModel):
    email: EmailStr


@router.post("/session", status_code=status.HTTP_201_CREATED)
async def crate_session(input: SessionInput):
    # uuid = create_session_from_email(input.email)
    return {"session": create_session_from_email(input.email)}
