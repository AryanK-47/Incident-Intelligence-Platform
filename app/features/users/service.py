import uuid
from fastapi import HTTPException,status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.features.users.models import User
from app.features.users import crud
from app.core.security import hash_password
from app.features.users.schemas import UserCreate, UserUpdate, UserResponse, RoleUserResponse


# User + roles = User Response
def build_user_response(user : User) -> RoleUserResponse:
    return RoleUserResponse(
        id= user.id,
        name = user.name,
        email=user.email,
        roles = [
            user_role.role.name
            for user_role in user.user_roles
        ]
    )

def create_user(db : Session , user : UserCreate):
    hashed_password = hash_password(user.password)

    try:
        created_user = crud.create_user(db,user, hashed_password)
        return build_user_response(created_user)

    except ValueError as e:
        message = str(e)

        if "email" in message:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail=message
            )
        
        if "role" in message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = message
            )
        raise

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = "User could not be created because of a database constraint conflict"
        )


def get_user(db : Session , user_id : uuid.UUID):
    user = crud.get_user(db, user_id)
    return build_user_response(user)


def delete_user(db : Session , user_id : uuid.UUID):
    user = crud.delete_user(db,user_id)
    return user


def update_user(db:Session, user_id : uuid.UUID, user_data : UserUpdate):
    data = user_data.model_dump(exclude_unset=True)

    if "password" in data:
        data["password_hash"] = hash_password(data["password"])
        del data["password"]

    return crud.update_user(db, user_id, data)
