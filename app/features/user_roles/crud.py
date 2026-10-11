import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.features.users.models import User
from app.features.roles.models import Role
from app.features.user_roles.models import UserRole

def create_user_role(
    db: Session,
    user_id: uuid.UUID,
    role_id: uuid.UUID
):
    # Check user exists and is active
    user = db.execute(
        select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None)
        )
    ).scalar_one_or_none()

    if user is None:
        return None, "USER_NOT_FOUND"

    # Check role exists
    role = db.get(Role, role_id)

    if role is None:
        return None, "ROLE_NOT_FOUND"

    # Check if role is already assigned
    existing = db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    ).scalar_one_or_none()

    if existing:
        return None, "ROLE_ALREADY_ASSIGNED"

    user_role = UserRole(
        user_id=user_id,
        role_id=role_id
    )

    db.add(user_role)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(user_role)

    return user_role, None


def update_user_role(
    db: Session,
    current_user_id : uuid.UUID,
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    new_role_id: uuid.UUID
):
    # Check user exists and is active
    user = db.execute(
        select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None)
        )
    ).scalar_one_or_none()

    if user is None:
        return None, "USER_NOT_FOUND"

    # Check existing role assignment
    user_role = db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    ).scalar_one_or_none()

    if user_role is None:
        return None, "ROLE_ASSIGNMENT_NOT_FOUND"

    # Check new role exists
    new_role = db.get(Role, new_role_id)

    if new_role is None:
        return None, "NEW_ROLE_NOT_FOUND"

    # Check if user already has the new role
    existing_new_role = db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == new_role_id
        )
    ).scalar_one_or_none()

    #If the role which need to be changed is *ADMIN*
    role = db.get(Role, role_id)
    if role.name == "ADMIN":

        # Cannot change another user's ADMIN role
        if current_user_id != user_id:
            return None, "CANNOT_CHANGE_OTHER_ADMIN"

        # Check if another ADMIN exists
        another_admin = db.execute(
            select(UserRole)
            .join(Role, UserRole.role_id == Role.id)
            .where(
                Role.name == "ADMIN",
                UserRole.user_id != current_user_id
            )
        ).scalar_one_or_none()
        
        # Current user is the last ADMIN
        if another_admin is None:
            return None, "CANNOT_CHANGE_LAST_ADMIN"


    if existing_new_role:
        return None, "NEW_ROLE_ALREADY_ASSIGNED"

    # Change the role
    user_role.role_id = new_role_id

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(user_role)

    return user_role, None

def delete_user_role(
    db: Session,
    current_user_id: uuid.UUID,
    user_id: uuid.UUID,
    role_id: uuid.UUID
):
    # Check user exists and is active
    user = db.execute(
        select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None)
        )
    ).scalar_one_or_none()

    if user is None:
        return None, "USER_NOT_FOUND"

    # Check existing role assignment
    user_role = db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    ).scalar_one_or_none()

    if user_role is None:
        return None, "ROLE_ASSIGNMENT_NOT_FOUND"

    # Get the role being removed
    role = db.get(Role, role_id)

    # ADMIN role protection
    if role.name == "ADMIN":

        # Cannot remove another user's ADMIN role
        if current_user_id != user_id:
            return None, "CANNOT_REMOVE_OTHER_ADMIN"

        # Check if another ADMIN exists
        another_admin = db.execute(
            select(UserRole)
            .join(Role, UserRole.role_id == Role.id)
            .where(
                Role.name == "ADMIN",
                UserRole.user_id != current_user_id
            )
        ).scalar_one_or_none()

        # Current user is the last ADMIN
        if another_admin is None:
            return None, "CANNOT_REMOVE_LAST_ADMIN"

    # Check how many roles the user currently has
    user_roles = db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id
        )
    ).scalars().all()

    # If this is the user's only role
    if len(user_roles) == 1:

        # If the only role is already VIEWER,
        # don't remove it because user must always have a role
        if role.name == "VIEWER":
            return user_role, None

        # Find VIEWER role for fallback
        viewer_role = db.execute(
            select(Role).where(
                Role.name == "VIEWER"
            )
        ).scalar_one_or_none()

        if viewer_role is None:
            return None, "VIEWER_ROLE_NOT_FOUND"

        # Replace the last role with VIEWER
        user_role.role_id = viewer_role.id

    else:
        # User has other roles, so normal deletion
        db.delete(user_role)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return user_role, None