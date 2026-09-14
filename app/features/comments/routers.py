from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.features.comments.schemas import CommentCreate, CommentResponse
from app.features.comments import service
import uuid

router = APIRouter()

# TODO: Derive user_id from the authenticated user instead of accepting it from the request
# TODO: Align comment route with final Incident router structure

@router.post("/incidents/{incident_id}/comments", response_model = CommentResponse)
def create_comment(
    comment : CommentCreate,
    user_id : uuid.UUID,
    incident_id : uuid.UUID,
    db : Session = Depends(get_db),
    ):

    return service.create_comment(db,comment,user_id, incident_id)
    

@router.get("/comments/{comment_id}", response_model = CommentResponse )
def get_comment(
    comment_id : uuid.UUID,
    db : Session = Depends(get_db)
    ):

    comment = service.get_comment(db, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment does not exist"
        )

    return comment
