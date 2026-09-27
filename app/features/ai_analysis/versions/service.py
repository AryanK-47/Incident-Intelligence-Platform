from sqlalchemy.orm import Session
import uuid
from app.features.ai_analysis.versions import crud
from app.features.ai_analysis import service

# Get a specific version
def get_version(db:Session, analysis_id : uuid.UUID, version_number : int):
    return crud.get_version(db, analysis_id,version_number)
