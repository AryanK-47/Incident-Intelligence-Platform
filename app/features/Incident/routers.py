from fastapi import APIRouter,Depends,HTTPException
import uuid
from app.features.Incident.models import Incident
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.features.Incident.schemas import IncidentCreate,IncidentResponse,IncidentUpdate
from app.features.Incident import service

router=APIRouter()

@router.post("/incidents",response_model=IncidentResponse)
def create_incident(incident_data:IncidentCreate, db:Session =Depends(get_db)):
    return service.create_incident(
        db=db,
        incident_data=incident_data,
        created_by=current_user.id
    )

@router.get("/incidents/{incident_id}",response_model=IncidentResponse)
def get_incident(incident_id:uuid.UUID,db:Session=Depends(get_db)):
    return service.get_incident(
        db=db,
        incident_id=incident_id
    )

@router.patch("/incidents/{incident_id}",response_model=IncidentResponse)
def update_incident(incident_id:uuid.UUID,
                    update_data:IncidentUpdate,
                    db:Session=Depends(get_db),
                    ):
    
    return service.update_incident(
        db=db,
        incident_id=incident_id,
        update_data=update_data,
    )

