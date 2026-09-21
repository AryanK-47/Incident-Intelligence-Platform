import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from .schemas import (
    IncidentAssigneeCreate,
    IncidentAssigneeResponse,
)
from . import service


router=APIRouter()

@router.post("/incidents/{incident.id}/assignees",response_model=IncidentAssigneeResponse)
def create_assigness(
    incident_id:uuid.UUID,
    assignment_data:IncidentAssigneeCreate,
    db:Session=Depends(get_db)
):
    