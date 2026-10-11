from fastapi import HTTPException, status
from app.features.user_roles import crud
from app.features.user_roles.schemas import UserRoleCreate, UserRoleUpdate


def create_user_role(db, user_id, role_data: UserRoleCreate):
    user_role, error = crud.create_user_role(
        db,
        user_id,
        role_data.role_id
    )

    if error == "USER_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if error == "ROLE_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    if error == "ROLE_ALREADY_ASSIGNED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role is already assigned to this user"
        )

    return user_role


def update_user_role(
    db,
    current_user_id,
    user_id,
    role_id,
    role_data: UserRoleUpdate
):
    user_role, error = crud.update_user_role(
        db,
        current_user_id,
        user_id,
        role_id,
        role_data.new_role_id
    )

    if error == "USER_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if error == "ROLE_ASSIGNMENT_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not have this role"
        )

    if error == "NEW_ROLE_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="New role not found"
        )

    if error == "NEW_ROLE_ALREADY_ASSIGNED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has this role"
        )

    if error == "CANNOT_CHANGE_OTHER_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An ADMIN cannot change another ADMIN's role"
        )

    if error == "CANNOT_CHANGE_LAST_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The last ADMIN cannot change their own role"
        )

    return user_role


def delete_user_role(
    db,
    current_user_id,
    user_id,
    role_id
):
    user_role, error = crud.delete_user_role(
        db,
        current_user_id,
        user_id,
        role_id
    )

    if error == "USER_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if error == "ROLE_ASSIGNMENT_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not have this role"
        )

    if error == "CANNOT_REMOVE_OTHER_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An ADMIN cannot remove another ADMIN's role"
        )

    if error == "CANNOT_REMOVE_LAST_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The last ADMIN cannot remove their own role"
        )

    if error == "VIEWER_ROLE_NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="System role VIEWER does not exist"
        )

    return user_role