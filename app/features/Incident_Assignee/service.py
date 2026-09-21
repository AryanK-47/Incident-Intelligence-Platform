import uuid

from sqlalchemy.orm import Session

from . import CRUD
from .schemas import IncidentAssigneeCreate
from .models import IncidentAssignee

def assign_user(
                db:Session,
                 incident_id:uuid.UUID,
                 assignment_data:IncidentAssigneeCreate,            ##isme direct usrid isliye ni kara kyoki infuture is class me or chzie add hogi to benefitial rhega
                 assigned_by:uuid.UUID)->IncidentAssignee:

    try:
        assignment=CRUD.assign_user(
            db=db,
            incident_id=incident_id,
            user_id=assignment_data.user_id,
            assigned_by=assigned_by
        )

        db.commit()
        db.refresh(assignment)

        return assignment

    except Exception:
        db.rollback()
        raise


def get_assignments(
        db:Session,
        incident_id:uuid.UUID
    )->list[IncidentAssignee]:

    return CRUD.get_assignments(                ##commit and refresh isliye ni kyoki kuch create ya modification nahi kr rhe hai 
        db=db,
        incident_id=incident_id
    )


def unassign_user(db:Session,
                  incident_id:uuid.UUID,
                  user_id:uuid.UUID)->IncidentAssignee:
    try:
        assignment= CRUD.unassign_user(db=db,
                                incident_id=incident_id,
                                user_id=user_id)

        db.commit()
        db.refresh(assignment)

        return assignment

    except Exception:
        db.rollback()
        raise
        

