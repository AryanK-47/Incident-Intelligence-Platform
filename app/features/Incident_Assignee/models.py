import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class IncidentAssignee(Base):
    __tablename__="incident_assignees"

    id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    incident_id:Mapped[uuid.UUID]=mapped_column(
        ForeignKey("incidents.id"),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(           ##kisko assign kiya
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_by: Mapped[uuid.UUID] = mapped_column(             ## kisne assign kiya
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    unassigned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )