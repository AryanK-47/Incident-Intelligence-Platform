from fastapi import APIRouter,Depends, HTTPException
from app.features.users import service
from app.features.users.schemas import UserResponse,UserCreate, UserUpdate
from app.core.database import get_db
from sqlalchemy.orm import Session
import uuid

router = APIRouter(prefix="/users")

@router.post("/", response_model = UserResponse)
def create_user(
    user : UserCreate,
    db: Session = Depends(get_db)
    ):
    
    return service.create_user(db,user)

@router.get("/{user_id}", response_model = UserResponse)
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
            response_model = UserResponse
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

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id : uuid.UUID,
                user_data : UserUpdate,
                db :Session = Depends(get_db)
            ):
    user = service.update_user(db, user_id, user_data)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    return user
    

    

