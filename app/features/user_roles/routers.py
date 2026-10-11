import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_admin
from app.features.users.models import User
from app.features.user_roles import service
from app.features.user_roles.schemas import (
    UserRoleCreate,
    UserRoleUpdate,
    UserRoleResponse,
)

router = APIRouter(
    prefix="/users",
    tags=["User Roles"],
)


@router.post(
    "/{user_id}/roles",
    response_model=UserRoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_role(
    user_id: uuid.UUID,
    role_data: UserRoleCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return service.create_user_role(
        db,
        user_id,
        role_data,
    )


@router.patch(
    "/{user_id}/roles/{role_id}",
    response_model=UserRoleResponse,
)
def update_role(
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    role_data: UserRoleUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return service.update_user_role(
        db,
        current_user.id,
        user_id,
        role_id,
        role_data,
    )


@router.delete(
    "/{user_id}/roles/{role_id}",
    response_model=UserRoleResponse,
)
def delete_role(
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return service.delete_user_role(
        db,
        current_user.id,
        user_id,
        role_id,
    )