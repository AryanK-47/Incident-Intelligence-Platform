import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends, HTTPException

from app.features.users import service
from app.core.database import get_db
from app.features.users.models import User
from app.core.permissions import require_admin,require_user_or_admin
from app.features.users.schemas import UserResponse,UserCreate, UserUpdate, RoleUserResponse

router = APIRouter(prefix="/users")

#CREATE ROUTERS
@router.post("/", response_model = RoleUserResponse)
def create_user(
    user : UserCreate,
    db: Session = Depends(get_db),
    current_admin : User = Depends(require_admin),
    ):
    
    return service.create_user(db,user)


#GET ROUTERS
@router.get("/{user_id}", response_model = RoleUserResponse)
def get_user(
    user_id : uuid.UUID,
    db : Session = Depends(get_db),
    current_user : User = Depends(require_user_or_admin)
    ):

    user = service.get_user(db, user_id)
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )
    
    return user


#UPDATE ROUTERS
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id : uuid.UUID,
                user_data : UserUpdate,
                db :Session = Depends(get_db),
                current_admin: User = Depends(require_admin)
            ):
    user = service.update_user(db, user_id, user_data)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    return service.build_user_response(user)


#DELETE ROUTERS
@router.delete("/{user_id}" ,
            response_model = UserResponse
        )
def delete_user(
    user_id : uuid.UUID,
    db : Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
    ):
    user = service.delete_user(db,user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    return service.build_user_response(user)


    

