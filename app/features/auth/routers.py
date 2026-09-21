from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.features.auth.services import get_token
from .schemas import LoginRequest,TokenResponse


router=APIRouter()

@router.post("/auth/login", response_model=TokenResponse)
def create_access(login:LoginRequest, 
                  db:Session=Depends(get_db)):
    return get_token(db=db,login=login)