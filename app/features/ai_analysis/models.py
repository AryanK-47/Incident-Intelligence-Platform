from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.features.Incident.models import Incident
    from app.features.ai_analysis.versions.models import AiAnalysisVersion


class AiAnalysis(Base):
    __tablename__="ai_analyses"
    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    incident_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("incidents.id"),
        unique=True,
        nullable=False
    )
    
    incident : Mapped["Incident"] = relationship(
        back_populates="ai_analysis"
    )
    current_version : Mapped[int] = mapped_column(
        nullable= False,
        default=1
    )

    versions : Mapped[list["AiAnalysisVersion"]] = relationship(
        back_populates="analysis"
    )
    

