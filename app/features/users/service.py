from sqlalchemy.orm import Session
from app.features.users.schemas import UserCreate, UserUpdate
from app.features.users import crud
from app.core.security import hash_password
import uuid

def create_user(db : Session , user : UserCreate):
    hashed_password = hash_password(user.password)

    return crud.create_user(db, user,hashed_password)

def get_user(db : Session , user_id : uuid.UUID):
    return crud.get_user(db, user_id)

def delete_user(db : Session , user_id : uuid.UUID):
    return crud.delete_user(db,user_id)

def update_user(db:Session, user_id : uuid.UUID, user_data : UserUpdate):
    data = user_data.model_dump(exclude_unset=True)

    if "password" in data:
        data["password_hash"] = hash_password(data["password"])
        del data["password"]

    return crud.update_user(db, user_id, data)
