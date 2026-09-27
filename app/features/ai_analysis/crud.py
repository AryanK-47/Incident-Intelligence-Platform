from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid
from app.features.ai_analysis.models import AiAnalysis
from app.features.ai_analysis.schemas import AiAnalysisCreate
from app.features.ai_analysis.versions.crud import create_version

from app.features.ai_analysis.versions.schemas import VersionCreate
from app.features.ai_analysis.versions.models import AiAnalysisVersion

#This returns complete deteails of the requested analysis
def get_analysis(db : Session , incident_id : uuid.UUID):
    statement = select(AiAnalysis).where(AiAnalysis.incident_id== incident_id)
    analysis = db.execute(statement).scalar_one_or_none()
    return analysis

#This creates a completely new analysis
def create_analysis(
        db : Session,
        incident_id : uuid.UUID,
        data : AiAnalysisCreate,
        version_number : int
        ):
    ai_analysis = AiAnalysis(
        incident_id=incident_id,
        current_version = version_number
    )
    db.add(ai_analysis)
    db.flush()


    create_version(db=db,
                    analysis_id=ai_analysis.id,
                    data=data.version,
                    version_number=version_number
                )

    db.commit()
    return ai_analysis

#This add a new version to analysis and updates current_analysis
def add_version(db:Session,
                analysis_id : uuid.UUID,
                data : VersionCreate,
                version_number : int
                ):
    create_version(db, analysis_id,data,version_number)
    statement = select(AiAnalysis).where(AiAnalysis.id==analysis_id)
    ai_analysis = db.execute(statement).scalar_one_or_none()
    ai_analysis.current_version=version_number

    db.commit()
    return ai_analysis

#This returns version number of current/latest version
def get_current_version_number(db : Session,
                                analysis_id : uuid.UUID
                            ):
    statement = select(AiAnalysis).where(AiAnalysis.id==analysis_id)
    ai_analysis = db.execute(statement).scalar_one_or_none()
    if ai_analysis is None:
        return None
    return ai_analysis.current_version

#This retuns list of available version numbers
def get_available_versions(db :Session , analysis_id : uuid.UUID):
    statement = (select(AiAnalysisVersion.version)
                .where(AiAnalysisVersion.analysis_id == analysis_id)
                .order_by(AiAnalysisVersion.version)
    )
    versions = db.execute(statement).scalars().all()

    return versions