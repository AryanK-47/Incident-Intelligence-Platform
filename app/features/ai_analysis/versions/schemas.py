from pydantic import BaseModel, ConfigDict, Field
import uuid
from datetime import datetime

class VersionBase(BaseModel):
    analysis_type : str = Field(...,
                                    description="type of analysis"
                                )

    root_cause : list[str] =Field(...,
                                    description="root cause of incident"
                                )

    root_cause_analysis : str = Field(...,
                                            description="analysis of root cause of incident"
                                        )

    suggested_remediation : list[str] = Field(...,
                                                description="Suggested remediations "
                                            )

    impact_analysis : str = Field(...,
                                    description="analysis of impact caused by incident"
                                )

    confidence : float = Field(...,
                                        description="confidence in analysis",
                                        ge=0.0,
                                        le=1.0
                                    )

    model : str = Field(..., description="model")


class VersionCreate(VersionBase):
    pass

class VersionResponse(VersionBase):
    model_config = ConfigDict(from_attributes=True)

    analysis_id : uuid.UUID = Field(...,
                                    description="analysis id"
                                )

    version : int = Field(...,
                            description="Verison number of analysis",
                            ge=1
                            )

    created_at : datetime

