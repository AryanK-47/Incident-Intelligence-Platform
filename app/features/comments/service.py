from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid

from app.features.comments.schemas import CommentCreate
from app.features.comments import crud
from app.features.Incident import CRUD as IncidentCRUD

def create_comment(db : Session,
                comment_data : CommentCreate,
                user_id : uuid.UUID,
                incident_id : uuid.UUID):

    incident = IncidentCRUD.get_incident(
        db=db,
        incident_id=incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return crud.create_comment(db, comment_data, user_id, incident_id)

def get_comment(db : Session, comment_id : uuid.UUID):
    return crud.get_comment(db,comment_id)

def get_incident_comments(db: Session, incident_id: uuid.UUID):

    # Check whether incident exists
    incident = IncidentCRUD.get_incident(
        db=db,
        incident_id=incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return crud.get_incident_comments(db, incident_id)