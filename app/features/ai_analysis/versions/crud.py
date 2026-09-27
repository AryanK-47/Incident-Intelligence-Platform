from sqlalchemy.orm import Session
from sqlalchemy import select, and_
import uuid
from app.features.ai_analysis.versions.schemas import VersionCreate
from app.features.ai_analysis.versions.models import AiAnalysisVersion

#This stores a new version in db
def create_version(
        db : Session,
        analysis_id : uuid.UUID,
        data : VersionCreate,
        version_number : int
        ):
    version = AiAnalysisVersion(
        analysis_id = analysis_id,
        version =version_number,
        analysis_type = data.analysis_type,
        root_cause = data.root_cause,
        root_cause_analysis = data.root_cause_analysis,
        suggested_remediation = data.suggested_remediation,
        impact_analysis = data.impact_analysis,
        confidence = data.confidence,
        model = data.model
    )

    db.add(version)
    db.flush()

    return version

#This retuns the version requested
def get_version(db : Session,
                analysis_id : uuid.UUID,
                version_number : int):
    statement = select(AiAnalysisVersion).where(
            and_(
                AiAnalysisVersion.analysis_id == analysis_id,
                AiAnalysisVersion.version==version_number
                )
            )
    version = db.execute(statement).scalar_one_or_none()

    return version