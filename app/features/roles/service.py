from sqlalchemy.orm import Session
from app.features.roles.schemas import RoleCreate, RoleUpdate
from app.features.roles import crud
import uuid

def create_role(db : Session, role_data : RoleCreate):
    return crud.create_role(db , role_data)

def get_role(db : Session , role_id : uuid.UUID):
    return crud.get_role(db, role_id)

def update_role(db : Session, role_id : uuid.UUID, role_data : RoleUpdate):
    return crud.update_role(db,role_id,role_data)