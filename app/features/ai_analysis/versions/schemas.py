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

    confidence: float | None = Field(
                                    default=None,
                                    description=(
                                        "Calibrated confidence estimate, when available. "
                                        "The RCA ranking score is not a confidence probability."
                                    ),
                                    ge=0.0,
                                    le=1.0,
                            )

    model : str = Field(..., description="model")

    rca_score: float | None = Field(
        default=None,
        description="V1 RCA ranking score; not a calibrated probability"
    )

    candidate_services: dict | list | None = Field(
        default=None,
        description="Ranked candidate services and their RCA scores"
    )

    evidence: dict | list | None = Field(
        default=None,
        description="Telemetry evidence and signal ranks supporting the RCA"
    )


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

