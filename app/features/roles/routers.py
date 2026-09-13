from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.features.roles.schemas import RoleCreate,RoleResponse
from app.features.roles import service
import uuid

router = APIRouter(prefix="/roles")

@router.post("/", response_model = RoleResponse)
def create_role(
        role_data : RoleCreate,
        db : Session = Depends(get_db)
    ):
    return service.create_role(db , role_data)

@router.get("/{role_id}", response_model = RoleResponse)
def get_role (
    role_id : uuid.UUID ,
    db : Session = Depends(get_db)
    ):
    role = service.get_role(db,role_id)

    if role is None:
        raise HTTPException(
            status_code = 404,
            detail = "Role does not exist"
        )

    return role

