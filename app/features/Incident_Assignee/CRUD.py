import uuid
from datetime import datetime,timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import IncidentAssignee

def assign_user(user_id:uuid.UUID,
                db:Session,
                assigned_by:uuid.UUID,
                incident_id:uuid.UUID)->IncidentAssignee:
    
    query=select(IncidentAssignee).where(
        IncidentAssignee.incident_id==incident_id,
        IncidentAssignee.user_id==user_id,
        IncidentAssignee.unassigned_at.is_(None)
    )
    result=db.execute(query).scalar_one_or_none()

    if result:
        raise ValueError("User is already assigned to this incident")

    assignment = IncidentAssignee(
        user_id=user_id,
        incident_id=incident_id,
        assigned_by=assigned_by,
    )
    db.add(assignment)
    db.flush()
    return assignment


def get_assignments(
        db:Session,
        incident_id:uuid.UUID,
        )->list[IncidentAssignee]:

    query=select(IncidentAssignee).where(
        IncidentAssignee.incident_id==incident_id
    )
    result=db.execute(query)

    return list(result.scalars().all())


def unassign_user(db:Session,
                  incident_id:uuid.UUID,
                  user_id:uuid.UUID)->IncidentAssignee:

    query=select(IncidentAssignee).where(
            IncidentAssignee.incident_id==incident_id,
            IncidentAssignee.user_id==user_id,
            IncidentAssignee.unassigned_at.is_(None)
        )
    result=db.execute(query).scalar_one_or_none()
    
    if result is None:
        raise ValueError("User is not assigned to this incident")

    result.unassigned_at = datetime.now(timezone.utc)
    db.flush()
    return result


    