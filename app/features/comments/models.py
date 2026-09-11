from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.features.users.models import User
    from app.features.Incident.models import Incident

class Comment(Base):
    __tablename__="comments"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default= uuid.uuid4
    )
    incident_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("incidents.id")
    )
    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id")
    )
    content : Mapped[str] = mapped_column(
        nullable=False
    )
    created_at : Mapped[datetime] = mapped_column(
        nullable=False,
        default= datetime.now
    )

    user : Mapped["User"] = relationship(
        back_populates="comments"
    )

    incident : Mapped["Incident"] = relationship(
        back_populates="comments"
    )