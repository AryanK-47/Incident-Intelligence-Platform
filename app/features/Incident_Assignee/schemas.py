from datetime import datetime
from pydantic import BaseModel, ConfigDict
import uuid

##incident id ni lenge kyoki vo url se ayegi
##assignest at automatic hoga
##unassignest at starting me null hoga
##assigned by current_login ke hisab se hoga

class IncidentAssigneeCreate(BaseModel):
    user_id:uuid.UUID

class IncidentAssigneeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    incident_id: uuid.UUID
    user_id: uuid.UUID
    assigned_by: uuid.UUID
    assigned_at: datetime
    unassigned_at: datetime | None