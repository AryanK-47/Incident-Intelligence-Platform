import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentEventResponse(BaseModel):
    id: uuid.UUID
    incident_id: uuid.UUID
    actor_id: uuid.UUID
    event_type: str
    old_value: str | None = None
    new_value: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)   