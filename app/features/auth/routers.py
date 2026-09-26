from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.services import get_token
from .schemas import LoginRequest, TokenResponse


router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
def create_access(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    return get_token(
        db=db,
        email=login_data.email,
        password=login_data.password
    )