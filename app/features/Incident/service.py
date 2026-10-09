from __future__ import annotations
from fastapi import HTTPException
import uuid
from app.core.metrics import CACHE_HITS, CACHE_MISSES, REDIS_ERRORS
from . import CRUD as IncidentCRUD
from app.features.Incident_Events import CRUD as EventCRUD
import json
import redis
from app.core.redis import (redis_client, build_incident_list_cache_key,invalidate_incident_list_cache,invalidate_incident_cache)
from datetime import datetime,timezone
from .schemas import (IncidentCreate, IncidentUpdate, IncidentStatus, Severity, IncidentListResponse, IncidentResponse)
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
        invalidate_incident_list_cache()

        db.refresh(new_incident)
        

        return new_incident

    except Exception:
         db.rollback()
         raise



def get_incident(
    db: Session,
    incident_id: uuid.UUID
) -> IncidentResponse:

    cache_key = f"incident:{incident_id}"

    try:
        cached_data = redis_client.get(cache_key)

        if cached_data:
            CACHE_HITS.labels(cache_type="single").inc()
            print("cache hit")

            return IncidentResponse(
                **json.loads(cached_data)
            )
        
        CACHE_MISSES.labels(cache_type="single").inc()
        
    except redis.RedisError:
        REDIS_ERRORS.labels(operation="get").inc()
        print("redis unavailable - falling back to database")

    print("cache miss or Redis unavailable")

    incident = IncidentCRUD.get_incident(
        db=db,
        incident_id=incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    response = IncidentResponse.model_validate(
        incident
    )

    try:
        redis_client.set(
            cache_key,
            response.model_dump_json(),
            ex=300,
        )

    except redis.RedisError:
        REDIS_ERRORS.labels(operation="set").inc()
        print("redis unavailable - response not cached")

    return response





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
        invalidate_incident_list_cache()
        
        invalidate_incident_cache(str(incident_id))

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



def get_incidents(
    db: Session,
    page: int,
    page_size: int,
    status: str | None = None,
    severity: str | None = None,
    service: str | None = None,
):
    cache_key = None
    cached_data = None
    
    try:
        cache_key = build_incident_list_cache_key(
                page=page,
                page_size=page_size,
                status=status,
                severity=severity,
                service=service,
            )
        
        cached_data = redis_client.get(cache_key)

        if cached_data:
            CACHE_HITS.labels(cache_type="list").inc()
            print("cache hit")
            return IncidentListResponse(**json.loads(cached_data))

        CACHE_MISSES.labels(cache_type="list").inc()
        
    except redis.RedisError:
        cached_data=None

    

    print("cache miss")

    incidents, total = IncidentCRUD.get_incidents(
        db=db,
        page=page,
        page_size=page_size,
        status=status,
        severity=severity,
        service=service,
    )
    cache_response=IncidentListResponse(
        items=[IncidentResponse.model_validate(incident)
               for incident in incidents],
        page=page,
        page_size=page_size,
        total=total,
    )

    if cache_key is not None:

        try:
            redis_client.set(
            cache_key,
            cache_response.model_dump_json(),
            ex=300
        )
        except redis.RedisError:
            print("redis unavailable - response not cached")

    return cache_response