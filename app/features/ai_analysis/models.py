from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, ARRAY, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

class AiAnalysis(Base):
    __tablename__="ai_analyses"
    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    incident_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("incidents.id")
    )
    analysis_type : Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    root_cause : Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable= False,
    )
    root_cause_analysis : Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    suggested_remediation : Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False
    )
    impact_analysis : Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    confidence : Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    model : Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


