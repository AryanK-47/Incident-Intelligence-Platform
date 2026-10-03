import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError

from app.features.users.models import User
from app.features.roles.models import Role
from app.features.user_roles.models import UserRole
from app.features.roles.schemas import RoleCreate,RoleUpdate, RoleUserResponse




def create_role(db : Session, role_data : RoleCreate):

    statement = select(Role).where(Role.name == role_data.name)
    existing = db.execute(statement).scalar_one_or_none()

    if existing:
        raise ValueError("This role already exist")
    
    role = Role(
        name = role_data.name
    )

    #Safety net check
    db.add(role)
    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise

    db.refresh(role)
    return role

def get_role(db : Session, role_id : uuid.UUID):

    statement = (
        select(Role)
        .options(
            selectinload(Role.user_roles)
            .selectinload(UserRole.user)
            .selectinload(User.user_roles)
            .selectinload(UserRole.role)

        )
        .where(Role.id == role_id)
    )
    
    result = db.execute(statement)

    return result.scalar_one_or_none()


def get_roles(db : Session):
    statement = select(Role).order_by(Role.name)
    result = db.execute(statement)
    return result.scalars().all()


def update_role(db : Session , role_id : uuid.UUID, role_data : RoleUpdate):

    data=role_data.model_dump(exclude_unset=True)

    #Check if data is empty
    if not data:
        raise ValueError("No field provided for update")


    #Check if the role with given id exists or not
    statement1 = select(Role).where(Role.id == role_id)
    role = db.execute(statement1).scalar_one_or_none()
    if role is None:
        return role

    #Admin role cannot be updated
    if role.name == "ADMIN":
        raise ValueError("System role cannot be changed")

    #Check if any role with same name exists
    statement2 = select(Role).where(Role.name == data["name"])
    existing = db.execute(statement2).scalar_one_or_none()
    if existing:
        raise ValueError("Role with this name already exists")

    role.name = data["name"]

    #Safety net check
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(role)
    return role

def delete_role(db: Session, role_id : uuid.UUID):

    role = db.get(Role,role_id)

    if role is None:
        return None

    if role.name == "ADMIN":
        raise ValueError("System role cannot be deleted")

    db.delete(role)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return role