from pydantic import Field, BaseModel,ConfigDict
import uuid
from app.features.ai_analysis.versions.schemas import VersionCreate, VersionResponse


class AiAnalysisCreate(BaseModel):
    version : VersionCreate = Field(
            description="All the required data of the current version"
        )


class AiAnalysisResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : uuid.UUID = Field(...,
                        description="analysis id"
                    )

    incident_id : uuid.UUID = Field(...,
                                            description="Incident id"
                                        )

    version : VersionResponse = Field(
            description="All the required data of the current version"
        )
    
    current_version : int = Field(...,
                                description="Latest version of analysis for the related incident",
                                ge =1
                                )


