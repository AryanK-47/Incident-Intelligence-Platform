import uuid
from fastapi import HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.features.users.models import User
from app.features.roles.models import Role
from app.features.user_roles.models import UserRole

def require_admin(
        current_user : User = Depends(get_current_user),
        db : Session = Depends(get_db),
)-> User:
    statement = (select(UserRole)
                .join(Role,UserRole.role_id == Role.id)
                .where(
                    UserRole.user_id == current_user.id,
                    Role.name == "ADMIN"
                )
    )
    user_role = db.execute(statement).scalar_one_or_none()

    if user_role is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Admin privileges required",
        )

    return current_user

def require_user_or_admin(
        user_id : uuid.UUID,
        current_user : User = Depends(get_current_user),
        db : Session = Depends(get_db),
)->User:

    #Admin can access any user
    statement = (
        select(Role)
        .join(UserRole)
        .where(
            UserRole.user_id == current_user.id,
            Role.name == "ADMIN"
        )
    )
    is_admin = db.execute(statement).scalar_one_or_none()

    if is_admin:
        return current_user

    #Normal user can access only their own record
    if current_user.id != user_id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="You can only access your own user profile."
        )

    #if current user is asking for its profile
    return current_user