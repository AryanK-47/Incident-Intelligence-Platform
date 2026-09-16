from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.roles import schemas
from app.features.roles.models import Role
import uuid

def create_role(db : Session, role_data : schemas.RoleCreate):

    role = Role(
        name = role_data.name
    )
    
    db.add(role)
    db.commit()
    db.refresh(role)

    return role

def get_role(db : Session, role_id : uuid.UUID):

    statement = select(Role).where(Role.id == role_id)
    
    result = db.execute(statement)

    return result.scalars().one_or_none()

def update_role(db : Session , role_id : uuid.UUID, role_data : schemas.RoleUpdate):

    role = db.get(Role, role_id)
    if role is None: return role

    data=role_data.model_dump(exclude_unset=True)

    for field,value in data.items():
        setattr(role, field ,value)

    db.commit()
    db.refresh(role)

    return role