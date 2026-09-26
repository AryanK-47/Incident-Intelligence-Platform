import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user

from .schemas import IncidentEventResponse
from .services import get_incident_events


router = APIRouter()


@router.get(
    "/incidents/{incident_id}/events",
    response_model=list[IncidentEventResponse]
)
def get_events(
    incident_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_incident_events(
        db=db,
        incident_id=incident_id
    )