import uuid

from sqlalchemy.orm import Session

from app.features.roles import crud
from app.features.roles.models import Role
from app.features.users.schemas import RoleUserResponse
from app.features.roles.schemas import RoleCreate, RoleUpdate, RoleDetailResponse


def _to_role_response(role : Role ) -> RoleDetailResponse:
    return RoleDetailResponse(
        id = role.id,
        name = role.name,
        users = [
            RoleUserResponse(
                id = user_role.user.id,
                name = user_role.user.name,
                email = user_role.user.email,
                roles = [ 
                    ur.role.name
                    for ur in user_role.user.user_roles
                    ]
            
                )
                for user_role in role.user_roles
            ]
        )

def create_role(db : Session, role_data : RoleCreate):
    return crud.create_role(db , role_data)

def get_role(db : Session , role_id : uuid.UUID):
    role = crud.get_role(db, role_id)

    if role is None:
        return None

    return _to_role_response(role)


def get_roles(db: Session):
    return crud.get_roles(db)

def update_role(db : Session, role_id : uuid.UUID, role_data : RoleUpdate):
    return crud.update_role(db,role_id,role_data)

def delete_role(db : Session, role_id : uuid.UUID):
    return crud.delete_role(db, role_id)

