from app.core.database import Base
from datetime import datetime,timezone,UTC
from app.features.Incident.models import Incident
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Incident_Events(Base):
    __tablename__="incident_events"

    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),
            default=uuid.uuid4,
            primary_key=True)
    
    incident_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("incidents.id"),nullable=False)

    actor_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id"),nullable=False)

    event_type:Mapped[str]=mapped_column(String, nullable=False)

    old_value:Mapped[str | None]=mapped_column(String,nullable=True)

    new_value:Mapped[str | None]=mapped_column(String,nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

