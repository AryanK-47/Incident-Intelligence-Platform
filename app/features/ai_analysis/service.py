from sqlalchemy.orm import Session
from app.features.ai_analysis import crud
from app.features.ai_analysis.schemas import AiAnalysisCreate, AiAnalysisResponse
import uuid
from app.features.Incident.service import get_incident
from app.features.ai_analysis.versions.service import get_version

#This returns a complete analysis
def get_analysis(db: Session, incident_id:uuid.UUID):
    incident = get_incident(db, incident_id)
    if incident is None: return None
    return crud.get_analysis(db,incident_id)

#This retuns current/latest versions number if exist or else none
def get_current_version_number(db:Session, incident_id : uuid.UUID):
    analysis =get_analysis(db, incident_id)
    if analysis is None: return None
    return analysis.current_version

'''This creates a new analysis
and checks if the analysis for given incident aready exists
If it does then simply add a version to this analysis
else create analysis as well as the version for it 
'''
def create_analysis(
        db : Session,
        incident_id : uuid.UUID,
        data : AiAnalysisCreate
        ):
    
    incident = get_incident(db, incident_id)
    if incident is None: return None

    analysis = get_analysis(db, incident_id)

    if analysis is None:
        version_number= 1
        return crud.create_analysis(db, incident_id,data,version_number)
    else:
        version_number = analysis.current_version+1
        return crud.add_version(db, analysis.id,data.version,version_number)

#This returns the complete ai-analysis which along with the latest version
def get_analysis_with_current_version(db : Session , incident_id : uuid.UUID):
    analysis = get_analysis(db, incident_id)

    if analysis is None :
        return None

    version = get_version(db, analysis.id, analysis.current_version)
    
    complete_analysis = AiAnalysisResponse(
            id = analysis.id,
            incident_id = incident_id,
            version = version,
            current_version=analysis.current_version
    )
    

    return complete_analysis
#This retuns list of available version numbers
def get_available_versions(db : Session, incident_id : uuid.UUID):
    analysis = get_analysis(db, incident_id)

    if analysis is None:
        return None
    
    return crud.get_available_versions(db,analysis.id)

def get_requested_version(db : Session, incident_id : uuid.UUID, version_number : int):

    analysis  = get_analysis(db, incident_id)
    if analysis is None: return None

    version = get_version(db, analysis.id, version_number)

    if version is None: return None
    return version