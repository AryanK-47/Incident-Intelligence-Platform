from __future__ import annotations
from fastapi import HTTPException
import uuid
from . import CRUD as IncidentCRUD
from app.features.Incident_Events import CRUD as EventCRUD
from datetime import datetime,timezone
from .schemas import IncidentCreate, IncidentUpdate, IncidentStatus, Severity
from sqlalchemy.orm import Session
from .schemas import IncidentCreate,IncidentUpdate,IncidentStatus
from .models import Incident


def create_incident(
    db: Session,
    incident_data: IncidentCreate,
    created_by: uuid.UUID
) -> Incident:

    try:
        new_incident = IncidentCRUD.create_incident(db=db,
                                incident_data=incident_data,
                                created_by=created_by
        )
        EventCRUD.create_event(db=db,
                       incident_id=new_incident.id,
                       actor_id=created_by,
                       event_type="INCIDENT_CREATED")

        db.commit()
        db.refresh(new_incident)
        

        return new_incident

    except Exception:
         db.rollback()
         raise

def get_incident(db:Session,incident_id:uuid.UUID)->Incident:

    incident=IncidentCRUD.get_incident(db=db, incident_id=incident_id)

    if incident is None:

        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


def update_incident(incident_id:uuid.UUID,update_data:IncidentUpdate,db:Session,actor_id:uuid.UUID)->Incident:

## pehle incident ko db se lao
    try:
        incident=IncidentCRUD.get_incident(db=db,
                           incident_id=incident_id)

        if incident is None:

            raise HTTPException(status_code=404, detail="Incident not found")

        if update_data.status is not None:
            current_status = IncidentStatus(incident.status)

            valid_status(current_status, update_data.status)

        if update_data.severity is not None:
            current_sev=Severity(incident.severity)
            


        if (
            update_data.status is not None
            and current_status != IncidentStatus.RESOLVED
            and update_data.status == IncidentStatus.RESOLVED
        ):
            incident.resolved_at = datetime.now(timezone.utc)

        IncidentCRUD.update_incident(
            db=db,
            update_data=update_data,
            incident=incident
        )

        if update_data.status is not None :
            EventCRUD.create_event(
                db=db,
                incident_id=incident_id,
                actor_id=actor_id,
                event_type="STATUS_CHANGED",
                old_value=current_status.value,
                new_value=update_data.status.value
            )
        if update_data.severity is not None and update_data.severity != current_sev:
            EventCRUD.create_event(
                db=db,
                incident_id=incident_id,
                actor_id=actor_id,
                event_type="SEVERITY_CHANGED",
                old_value=current_sev.value,
                new_value=update_data.severity.value
            )

        db.commit()
        db.refresh(incident)
        return incident
    
    except Exception:
        db.rollback()
        raise

ALLOWED_TRANSITIONS = {
    IncidentStatus.OPEN: {
        IncidentStatus.INVESTIGATING
    },

    IncidentStatus.INVESTIGATING: {
        IncidentStatus.IDENTIFIED,
        IncidentStatus.MITIGATING
    },

    IncidentStatus.IDENTIFIED: {
        IncidentStatus.MITIGATING
    },

    IncidentStatus.MITIGATING: {
        IncidentStatus.INVESTIGATING,
        IncidentStatus.RESOLVED
    },

    IncidentStatus.RESOLVED: {
        IncidentStatus.CLOSED
    },

    IncidentStatus.CLOSED: set()
}

def valid_status(current_status:IncidentStatus,new_status:IncidentStatus):
    allowed_status=ALLOWED_TRANSITIONS[current_status]

    if new_status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition: "
                   f"{current_status.value} -> {new_status.value}")
