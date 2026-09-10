from enum import Enum
import uuid
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel,Field

class Severity(str,Enum):
    SEV1="SEV1"
    SEV2="SEV2"
    SEV3="SEV3"
    SEV4="SEV4"

class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    IDENTIFIED = "IDENTIFIED"
    MITIGATING = "MITIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class IncidentCreate(BaseModel):
    title : Annotated[
        str,Field(...,min_length=1,max_length=200)
    ]
    description: Annotated[
        str,Field(...,min_length=10)
    ]
    service: Annotated[
        str,Field(...,min_length=1,max_length=100)
    ]
    severity: Severity

class IncidentUpdate(BaseModel):
        title : Annotated[
                str| None,Field(default=None,min_length=1,max_length=200)
            ]
        description: Annotated[
                str| None,Field(default=None,min_length=10)
            ]
        service: Annotated[
                str| None,Field(default=None,min_length=1,max_length=100)
            ]
        
        severity: Severity | None=None

        cause: Annotated[
             str | None, Field(default=None,min_length=5)]

        status : IncidentStatus | None =None

class IncidentResponse(BaseModel):

    id: uuid.UUID

    title: str

    description: str

    service: str

    severity: Severity

    status: IncidentStatus

    cause: str | None

    created_by: uuid.UUID

    created_at: datetime

    resolved_at: datetime | None