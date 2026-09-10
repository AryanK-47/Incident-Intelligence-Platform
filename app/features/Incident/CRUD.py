import uuid
from enum import Enum
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.Incident.models import Incident
from app.features.Incident.schemas import IncidentCreate,IncidentUpdate


def create_incident(incident_data:Incident, db:Session,created_by:uuid.UUID)->Incident:
    new_data=Incident(
        title=incident_data.title,
        description=incident_data.description,
        service=incident_data.service,
        severity=incident_data.severity
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data


def get_incident(db:Session,incident_id:uuid.UUID)->Incident | None:
    query=select(Incident).where(Incident.id==incident_id)
    result=db.execute(query)

    info=result.scalar_one_or_none()

    return info


def update_incident(db:Session, update_data:IncidentUpdate, incident:Incident):
    data=update_incident.modal_dump(exclude_unset=True)

    for fields,values in data.items():

        if isinstance(values,Enum):
            values=values.value

        setattr(incident,fields,values)

    db.commit()
    db.refresh(incident)

    return incident
