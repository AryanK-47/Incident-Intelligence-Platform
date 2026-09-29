import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timezone

from app.features.users.models import User
from app.features.roles.models import Role
from app.features.users.schemas import UserCreate
from app.features.user_roles.models import UserRole


def create_user(db : Session,
                user_data : UserCreate,
                hashed_password : str
            ):

    # Check duplicate email
    existing_user = db.execute(
        select(User).where(User.email == user_data.email)
    ).scalar_one_or_none()
    if existing_user:
        raise ValueError(
            "A user with this email already exists."
        )


    #To get the id of role entered by user
    role = db.execute(
        select(Role).where(Role.name == user_data.role)
        ).scalar_one_or_none()
    if role is None:
        raise ValueError(f"Invalid role. {user_data.role}")


    # Create SQLAlchemy User model
    user = User(
        name = user_data.name,
        email = user_data.email,
        password_hash = hashed_password
    )

    db.add(user)
    db.flush()

    # Create UserRole association
    user_role = UserRole(
        user_id = user.id,
        role_id = role.id
    )

    db.add(user_role)
    
    try :
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(user)

    return user

def get_user(db : Session, user_id : uuid.UUID):
    statement = select(User).where(
        User.id==user_id,
        User.deleted_at.is_(None))
    result = db.execute(statement)
    return result.scalars().one_or_none()

def delete_user(db :Session , user_id : uuid.UUID):

    statement = select(User).where(
                                User.id == user_id,
                                User.deleted_at.is_(None))
    user = db.execute(statement).scalars().one_or_none()

    if user is None : return None
    
    user.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)

    return user


def update_user(db : Session , user_id : uuid.UUID, data : dict):
    statement = select(User).where(
        User.id == user_id,
        User.deleted_at.is_(None)
    )
    user = db.execute(statement).scalar_one_or_none()

    if user is None: return user

    
    for field, value in data.items():
        setattr(user,field,value)

    db.commit()
    db.refresh(user)

    return user