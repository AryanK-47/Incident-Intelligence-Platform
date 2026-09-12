from pydantic import Field, BaseModel,ConfigDict
import uuid
from datetime import datetime

class AiAnalysisResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : uuid.UUID = Field(...,
                        description="analysis id"
                    )

    incident_id : uuid.UUID = Field(...,
                                    description="Incident id"
                                )
    
    analysis_type : str = Field(...,
                                description="type of analysis"
                            )
    
    root_cause : list[str] =Field(...,
                                description="root cause of incident"
                            )
    
    suggested_remediation : list[str] = Field(...,
                                            description="Suggested remediations "
                                        )
    impact_analysis : str = Field(...,
                                description="analysis of impact caused by incident"
                            )
    
    model : str = Field(..., description="model")

    created_at : datetime

    root_cause_analysis : str = Field(...,
                                    description="analysis of root cause of incident"
                                )
    
    confidence : float = Field(...,
                            description="confidence in analysis",
                            ge=0.0,
                            le=1.0
                        )


