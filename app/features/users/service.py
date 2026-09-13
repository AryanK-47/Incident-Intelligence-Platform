from sqlalchemy.orm import Session
from app.features.users.schemas import UserCreate
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