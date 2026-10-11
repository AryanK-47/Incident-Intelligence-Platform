import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.features.users.models import User

from .schemas import IncidentAssigneeCreate, IncidentAssigneeResponse
from . import service

router = APIRouter(tags=["Incident Assignees"])


@router.post(
    "/incidents/{incident_id}/assignees",
    response_model=IncidentAssigneeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assignee(
    incident_id: uuid.UUID,
    assignment_data: IncidentAssigneeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.assign_user(
            db=db,
            incident_id=incident_id,
            assignment_data=assignment_data,
            assigned_by=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/incidents/{incident_id}/assignees",
    response_model=list[IncidentAssigneeResponse],
)
def list_assignees(
    incident_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_assignments(
        db=db,
        incident_id=incident_id,
    )


@router.delete(
    "/incidents/{incident_id}/assignees/{user_id}",
    response_model=IncidentAssigneeResponse,
)
def remove_assignee(
    incident_id: uuid.UUID,
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.unassign_user(
            db=db,
            incident_id=incident_id,
            user_id=user_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc