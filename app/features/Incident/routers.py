from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.features.Incident.schemas import IncidentCreate

router=APIRouter()

@router.post("/incidents")
def create_incident(incident_data:IncidentCreate, db:Session =Depends(get_db)):
    return incident_data