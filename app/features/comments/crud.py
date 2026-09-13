from sqlalchemy.orm import Session
from sqlalchemy import select
from app.features.comments.schemas import CommentCreate
from app.features.comments.models import Comment
import uuid



def create_comment(
        db : Session,
        comment_data : CommentCreate,
        user_id : uuid.UUID ,
        incident_id : uuid.UUID
    ):

    comment = Comment (
        incident_id = incident_id,
        user_id = user_id,
        content = comment_data.content
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

def get_comment(db : Session, comment_id : uuid.UUID):

    statement = select(Comment).where(Comment.id == comment_id)
    result = db.execute(statement).scalars().one_or_none()

    return result
