import uuid

from sqlalchemy.orm import Session

from app.features.Incident_Events import CRUD


def get_incident_events(
    db: Session,
    incident_id: uuid.UUID
):
    return CRUD.get_events_by_incidents(db=db,
        incident_id=incident_id
    )