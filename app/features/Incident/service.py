from __future__ import annotations
from fastapi import HTTPException
import uuid
from . import CRUD
from datetime import datetime,timezone
from sqlalchemy.orm import Session
from .schemas import IncidentCreate,IncidentUpdate,IncidentStatus
from .models import Incident


def create_incident(
    db: Session,
    incident_data: IncidentCreate,
    created_by: uuid.UUID
) -> Incident:

    new_incident = CRUD.create_incident(db=db,
                                        incident_data=incident_data,
                                        created_by=created_by
    )

    db.commit()
    db.refresh(new_incident)
    

    return new_incident

def get_incident(db:Session,incident_id:uuid.UUID)->Incident:
    incident=CRUD.get_incident(db=db, incident_id=incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


def update_incident(incident_id:uuid.UUID,update_data:IncidentUpdate,db:Session)->Incident:

## pehle incident ko db se lao
    try:
        incident=CRUD.get_incident(db=db,
                                incident_id=incident_id)

        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        if update_data.status is not None:
            current_status=IncidentStatus(incident.status)
            valid_status(current_status,update_data.status)
            
        if(update_data.status is not None and 
                current_status != IncidentStatus.RESOLVED and
                update_data.status==IncidentStatus.RESOLVED):
                    
                    incident.resolved_at=datetime.now(timezone.utc)

        ## db se lane ke bad isko ab update karo
        CRUD.update_incident(db=db,
                            update_data=update_data,
                            incident=incident)


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
