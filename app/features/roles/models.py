from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.features.user_roles.models import UserRole
class Role(Base):

    __tablename__ = "roles"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True
        )
    name : Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )

    user_roles : Mapped[list["UserRole"]] = relationship(
        back_populates="role",
        cascade= "all,delete-orphan"
    )