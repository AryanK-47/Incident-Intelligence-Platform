import uuid
from enum import Enum
from app.features.Incident_Events.models import Incident_Events
from sqlalchemy import select
from sqlalchemy.orm import Session



def create_event(
        db:Session,
        incident_id:uuid.UUID,
        actor_id:uuid.UUID,
        event_type:str,
        old_value:str | None=None,
        new_value:str | None=None,
)->Incident_Events:

    event=Incident_Events(
        incident_id=incident_id,
        actor_id=actor_id,
        event_type=event_type,
        old_value=old_value,
        new_value=new_value
    )
    db.add(event)
    db.flush()

    return event
    
    