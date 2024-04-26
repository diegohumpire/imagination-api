import uuid

from ..databases.redis_db import get_redis_connection

redis = get_redis_connection()

EMAIL_KEY: str = "emails"
SESSION_KEY: str = "sessions"
TTL_SESSION_SECONDS: int = 600


def __email_prefix(email: str) -> str:
    return f"{EMAIL_KEY}:{email}"


def __session_prefix(uuid: str) -> str:
    return f"{SESSION_KEY}:{uuid}"


def create_session_from_email(email: str) -> str:
    """
    Creates a session for the given email.

    Args:
        email (str): The email address to create a session for.

    Returns:
        str: The session ID generated for the email.

    """
    if session_exists_by_email(email):
        return get_session_by_email(email)

    uuid_ = str(uuid.uuid4())
    redis.set(__email_prefix(email), uuid_, ex=TTL_SESSION_SECONDS)
    redis.set(__session_prefix(uuid_), email, ex=TTL_SESSION_SECONDS)

    return uuid_


def session_exists_by_email(email: str) -> bool:
    """
    Checks if a session exists for the given email.

    Args:
        email (str): The email address to check for a session.

    Returns:
        bool: True if a session exists for the email, False otherwise.

    """
    return redis.exists(__email_prefix(email))


def session_exists_by_uuid(uuid_: str) -> bool:
    """
    Checks if a session exists for the given UUID.

    Args:
        uuid_ (str): The UUID to check for a session.

    Returns:
        bool: True if a session exists for the UUID, False otherwise.

    """
    return redis.exists(__session_prefix(uuid_))


def get_session_email_by_uuid(uuid_: str) -> str:
    """
    Gets the email associated with the given session UUID.

    Args:
        uuid_ (str): The UUID to get the associated email for.

    Returns:
        str: The email address associated with the session.

    """
    return str(redis.get(__session_prefix(uuid_)))


def get_session_by_email(email: str) -> str:
    """
    Gets the session associated with the given email address.

    Args:
        email (str): The email address to get the associated session for.

    Returns:
        str: The session ID associated with the email.

    """
    return redis.get(__email_prefix(email))
