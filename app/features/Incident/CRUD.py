import uuid
from enum import Enum

from sqlalchemy import select,func
from sqlalchemy.orm import Session

from app.features.Incident.models import Incident
from app.features.Incident.schemas import IncidentCreate,IncidentUpdate


def create_incident(incident_data:IncidentCreate,
                     db:Session,
                     created_by:uuid.UUID)->Incident:
    new_data=Incident(
        title=incident_data.title,
        description=incident_data.description,
        service=incident_data.service,
        severity=incident_data.severity.value,
        created_by=created_by
    )
    db.add(new_data)
    db.flush()

    return new_data


def get_incident(db:Session,incident_id:uuid.UUID)->Incident | None:
    query=select(Incident).where(Incident.id==incident_id)
    result=db.execute(query)

    info=result.scalar_one_or_none()

    return info


def update_incident(db:Session, 
                    update_data:IncidentUpdate, 
                    incident:Incident):
    
    data = update_data.model_dump(exclude_unset=True)

    for fields,values in data.items():
        if isinstance(values,Enum):
            values=values.value

        setattr(incident,fields,values)

    ## db.add() isliye nhi kiya kyoki vo incident ya data vo pehle se hi sqlalchemy me managed object hai , ye chiz koi naya add on krna hota hai uske liye hota hai
    db.flush()

    return incident


def get_incidents(db:Session,
                  page:int,
                  page_size:int,
                  status: str | None = None,
                  severity: str | None = None,
                  service:str | None =None,):

    query=select(Incident)

    if status is not None:
        if isinstance(status, Enum):
            status = status.value
        query=query.where(Incident.status==status)

    if severity is not None:
        if isinstance(severity, Enum):
            severity = severity.value
        query=query.where(Incident.severity==severity)

    if service is not None:
        if isinstance(service, Enum):
            service = service.value
        query=query.where(Incident.service==service)


    query=( 
        query.order_by(Incident.created_at.desc()).offset( (page-1) * page_size).limit(page_size)
    )

    result=db.execute(query)

    incidents=result.scalars().all()

    count_query=select(func.count()).select_from(Incident)

    if status is not None:
        if isinstance(status, Enum):
            status = status.value
        count_query=count_query.where(Incident.status==status)
    
    if severity is not None:
        if isinstance(severity, Enum):
            severity = severity.value
        count_query=count_query.where(Incident.severity==severity)
    
    if service is not None:
        if isinstance(service, Enum):
            service = service.value
        count_query=count_query.where(Incident.service==service)

    total=db.execute(count_query).scalar_one()

    return incidents,total

                    