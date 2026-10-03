import uuid

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status

from app.core.database import get_db
from app.features.roles import service
from app.features.users.models import User
from app.core.auth import get_current_user
from app.core.permissions import require_admin, require_user_or_admin
from app.features.roles.schemas import RoleCreate,RoleResponse, RoleUpdate, RoleDetailResponse



router = APIRouter(prefix="/roles")


#CREATE ROUTERS
@router.post("/", response_model = RoleResponse)
def create_role(
        role_data : RoleCreate,
        db : Session = Depends(get_db),
        current_admin :User = Depends(require_admin)
    ):
    try :
        return service.create_role(db , role_data)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail= str(e)
        )


#GET ROUTERS
@router.get("/" , response_model= list[RoleResponse])
def get_roles(db : Session = Depends(get_db),
                current_admin : User = Depends(get_current_user)
            ):
    return service.get_roles(db)


@router.get("/{role_id}", response_model = RoleDetailResponse)
def get_role (
    role_id : uuid.UUID ,
    db : Session = Depends(get_db),
    current_admin : User = Depends(require_admin)
    ):
    role = service.get_role(db,role_id)

    if role is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Role does not exist"
        )

    return role



#UPDATE/PATCH ROUTERS
@router.patch("/{role_id}", response_model= RoleResponse)
def update_role(role_id : uuid.UUID,
                role_data : RoleUpdate,
                db : Session = Depends(get_db),
                current_admin : User = Depends(require_admin)
            ):
    try :
        role = service.update_role(db, role_id, role_data)

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role does not exist")

        return role

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = str(e)
        )


#DELETE ROUTERS
@router.delete("/{role_id}", response_model= RoleResponse)
def delete_role(
    role_id : uuid.UUID,
    db : Session = Depends(get_db),
    current_ : User = Depends(require_admin)
):

    try:
        role = service.delete_role(db, role_id)

        if role is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Role does not exist"
                    )
        return role

        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= str(e)
        )

