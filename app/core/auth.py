from datetime import datetime,timezone,timedelta
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.users.models import User
import jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(user_id:str)->str:
    expires=datetime.now(timezone.utc)+timedelta(
        minutes=settings.EXPIRATION
    )
    payload={
        "sub":user_id,
        "exp":expires
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )




def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
        )->User:

    ##signature + exp validation part
    try:
        payload=jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expire token")

    user_id=payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        user_uuid = uuid.UUID(user_id)
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
        )

    user=db.get(User,user_uuid)

    if user is None or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user