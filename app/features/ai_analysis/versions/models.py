from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String,ARRAY,Text,Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime,timezone

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.features.ai_analysis.models import AiAnalysis


class AiAnalysisVersion(Base):
    __tablename__= "ai_analysis_versions"

    analysis_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ai_analyses.id"),
        primary_key=True
    )

    version : Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        primary_key=True
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
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    analysis : Mapped["AiAnalysis"] = relationship(
        back_populates = "versions"
    )