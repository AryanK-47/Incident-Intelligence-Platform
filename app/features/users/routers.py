from fastapi import APIRouter,Depends, HTTPException
from app.features.users import schemas,service
from app.core.database import get_db
from sqlalchemy.orm import Session
import uuid

router = APIRouter(prefix="/users")

@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user : schemas.UserCreate,
    db: Session = Depends(get_db)
    ):
    
    return service.create_user(db,user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id : uuid.UUID,
    db : Session = Depends(get_db)
    ):

    user = service.get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )
    
    return user

@router.delete("/{user_id}" ,
            response_model= schemas.UserResponse
        )
def delete_user(
    user_id : uuid.UUID,
    db : Session = Depends(get_db)
    ):
    user = service.delete_user(db,user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    return user
    

