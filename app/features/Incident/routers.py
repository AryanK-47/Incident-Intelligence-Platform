from fastapi import APIRouter,Depends,HTTPException,Query
from app.core.auth import get_current_user
from app.features.users.models import User
import uuid
from app.features.Incident.models import Incident
from sqlalchemy.orm import Session
from .schemas import IncidentListResponse, IncidentStatus, Severity
from app.core.database import get_db
from app.features.Incident.schemas import IncidentCreate,IncidentResponse,IncidentUpdate
from app.features.Incident import service as incident_service

router=APIRouter()

@router.post("/incidents",response_model=IncidentResponse)
def create_incident(incident_data:IncidentCreate,
                     db:Session =Depends(get_db),
                     current_user:User=Depends(get_current_user)):
    return incident_service.create_incident(
        db=db,
        incident_data=incident_data,
        created_by=current_user.id
    )

@router.get("/incidents", response_model=IncidentListResponse)
def get_incidents(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: IncidentStatus | None = None,
    severity: Severity | None = None,
    service: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incidents, total = incident_service.get_incidents(
        db=db,
        page=page,
        page_size=page_size,
        status=status,
        severity=severity,
        service=service,
    )

    return {
        "items": incidents,
        "page": page,
        "page_size": page_size,
        "total": total,
    }

@router.get("/incidents/{incident_id}",response_model=IncidentResponse)
def get_incident(incident_id:uuid.UUID,
                 db:Session=Depends(get_db),
                 current_user:User=Depends(get_current_user),):
    return incident_service.get_incident(
        db=db,
        incident_id=incident_id
    )

@router.patch("/incidents/{incident_id}",response_model=IncidentResponse)
def update_incident(incident_id:uuid.UUID,
                    update_data:IncidentUpdate,
                    db:Session=Depends(get_db),
                    current_user:User=Depends(get_current_user),
                    ):
    
    return incident_service.update_incident(
        db=db,
        incident_id=incident_id,
        update_data=update_data,
        actor_id=current_user.id
    )

