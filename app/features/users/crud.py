from sqlalchemy.orm import Session
from sqlalchemy import select
from app.features.users.schemas import UserCreate
from app.features.users.models import User
import uuid
from datetime import datetime, timezone


def create_user(db : Session , user_data : UserCreate, hashed_password : str):
    user = User(
        name = user_data.name,
        email = user_data.email,
        password_hash = hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user(db : Session, user_id : uuid.UUID):
    statement = select(User).where(User.id==user_id)
    result = db.execute(statement)
    return result.scalars().one_or_none()

def delete_user(db :Session , user_id : uuid.UUID):

    statement = select(User).where(User.id == user_id)
    user = db.execute(statement).scalars().one_or_none()

    if user is None : return None
    
    user.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)

    return user


def update_user(db : Session , user_id : uuid.UUID, data : dict):
    user = db.get(User,user_id)
    if user is None: return user

    
    for field, value in data.items():
        setattr(user,field,value)

    db.commit()
    db.refresh(user)

    return user