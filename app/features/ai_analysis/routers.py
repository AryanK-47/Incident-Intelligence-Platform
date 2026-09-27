import uuid

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.ai_analysis import service
from app.features.ai_analysis.schemas import (
    AiAnalysisCreate,
    AiAnalysisResponse,
)
from app.features.ai_analysis.versions.schemas import VersionResponse

router = APIRouter()

@router.post("/incidents/{incident_id}/ai-analysis",
            response_model=AiAnalysisResponse
        )
def create_analysis(data : AiAnalysisCreate,
                    incident_id : uuid.UUID,
                    db : Session = Depends(get_db)
                    ):
    
    analysis = service.create_analysis(db, incident_id,data)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Incident for this id does not exist"
        )
    return analysis


@router.get("/incidents/{incident_id}/ai-analysis",
            response_model=AiAnalysisResponse
            )

def get_analysis(incident_id : uuid.UUID,
                db : Session = Depends(get_db)
                ):
    analysis = service.get_analysis_with_current_version(db, incident_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail='''No such incident for the given incident id
                                    or
                        Analysis does not exist for this incident
            '''
        )
    return analysis

@router.get("/incidents/{incident_id}/ai-analysis/versions",
            response_model= list[int])
def get_available_versions(incident_id : uuid.UUID,
                            db : Session = Depends(get_db)
                        ):
    versions = service.get_available_versions(db, incident_id)

    if versions is None:
        raise HTTPException(
            status_code=404,
            detail='''No such incident for the given incident id
                                    or
                        Analysis does not exist for this incident
            '''
        )
    
    return versions

@router.get("/incidents/{incident_id}/ai-analysis/versions/{version_number}",
            response_model=VersionResponse)
def get_requested_version(
    incident_id : uuid.UUID,
    version_number : int = Path(..., ge=1),
    db : Session = Depends(get_db)
    ):
    version = service.get_requested_version(db, incident_id,version_number)

    if version is None:
        raise HTTPException(
            status_code= 404,
            detail='''No such incident for the given incident id
                                        or
                        Analysis does not exist for this incident
                                        or
                        No such version exists for the given number
            '''
        )
    return version