from typing import Annotated

from fastapi import HTTPException, Header, status

from main.services.sessions import session_exists_by_uuid


def check_session(x_session_token: Annotated[str, Header()]):
    if not session_exists_by_uuid(x_session_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")

    yield x_session_token
