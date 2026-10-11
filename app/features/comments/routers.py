from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.core.auth import get_current_user
from app.core.database import get_db
from app.features.users.models import User
from app.features.comments.schemas import CommentCreate, CommentResponse
from app.features.comments import service

router = APIRouter()


@router.post(
    "/incidents/{incident_id}/comments",
    response_model=CommentResponse,
)
def create_comment(
    incident_id: uuid.UUID,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_comment(
        db=db,
        comment_data=comment,
        user_id=current_user.id,
        incident_id=incident_id,
    )


@router.get(
    "/incidents/{incident_id}/comments",
    response_model=list[CommentResponse],
)
def get_incident_comments(
    incident_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_incident_comments(
        db=db,
        incident_id=incident_id,
    )


@router.get(
    "/comments/{comment_id}",
    response_model=CommentResponse,
)
def get_comment(
    comment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = service.get_comment(db, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment does not exist",
        )

    return comment