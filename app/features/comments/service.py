from sqlalchemy.orm import Session
from app.features.comments.schemas import CommentCreate
from app.features.comments import crud
import uuid

def create_comment(db : Session , comment_data : CommentCreate, user_id : uuid.UUID, incident_id : uuid.UUID):
    return crud.create_comment(db, comment_data, user_id, incident_id)

def get_comment(db : Session, comment_id : uuid.UUID):
    return crud.get_comment(db,comment_id)