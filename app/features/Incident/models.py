import uuid
from datetime import datetime,timezone

from app.core.database import Base
from sqlalchemy.orm import Mapped,MappedColumn
from sqlalchemy import String,Text,ForeignKey,PrimaryKeyConstraint,Integer,DateTime

class Incident(Base):
    __tablename__='incidents'

    id:Mapped[uuid.UUID]=MappedColumn(primary_key=True,default=uuid.uuid4)
    
    title:Mapped[str]=MappedColumn(String(200),nullable=False)
    description:Mapped[str]=MappedColumn(Text,nullable=False)
    service:Mapped[str]=MappedColumn(String(20),nullable=False)
    severity:Mapped[str]=MappedColumn(String(10),nullable=False)
    status:Mapped[str]=MappedColumn(String(15),nullable=False,default="OPEN")
    cause:Mapped[str]=MappedColumn(Text,nullable=True)
    created_at:Mapped[datetime]=MappedColumn(DateTime(timezone=True),nullable=False,default=lambda:datetime.now(timezone.utc))
    created_by:Mapped[uuid.UUID]=MappedColumn(ForeignKey("users.id"),nullable=False)
    resolved_at: Mapped[datetime | None] = MappedColumn(DateTime(timezone=True),nullable=True)
