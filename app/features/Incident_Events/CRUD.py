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

def get_events_by_incidents(db:Session,
                            incident_id:uuid.UUID,
                            )->list[Incident_Events]:
    query=select(Incident_Events).where(Incident_Events.incident_id==incident_id).order_by(Incident_Events.created_at)

    result=db.execute(query)

    return list(result.scalars().all())
    
    