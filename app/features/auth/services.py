from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.security import verify_password
from app.features.users.models import User

from .schemas import LoginRequest, TokenResponse

def get_token(db: Session, email: str, password: str):

    result = select(User).where(User.email == email)
    query = db.execute(result).scalar_one_or_none()

    if query is None or query.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password(password, query.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(str(query.id))

    return TokenResponse(access_token=token)