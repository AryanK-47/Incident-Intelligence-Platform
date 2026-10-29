from sqlalchemy.orm import Session, selectinload
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

    statement = (
        select(Comment)
        .options(selectinload(Comment.user))
        .where(Comment.id == comment_id)
    )

    result = db.execute(statement)
    return result.scalars().one_or_none()

##Ye function ek incident ke saare comments oldest-first return karega.
def get_incident_comments(db: Session, incident_id: uuid.UUID):
    statement = (
        select(Comment)
        .options(selectinload(Comment.user))
        .where(Comment.incident_id == incident_id)
        .order_by(Comment.created_at.asc())
    )

    result = db.execute(statement)
    return list(result.scalars().all())
