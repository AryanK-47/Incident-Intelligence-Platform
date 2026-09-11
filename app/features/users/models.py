from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.features.roles.models import Role
    from app.features.comments.models import Comment


class User(Base):
    __tablename__="users"
    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
        )
    name : Mapped[str] = mapped_column(nullable=False)
    email : Mapped[str] = mapped_column(
        unique=True,
        nullable=False)
    password_hash : Mapped[str] = mapped_column(nullable=False)
    created_at : Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now)
    deleted_at : Mapped[datetime | None] = mapped_column(default=None)

    roles : Mapped[list["Role"]] = relationship(
        secondary="user_roles",
        back_populates="users"
    )

    comments : Mapped[list["Comment"]] = relationship(
        back_populates="user"
    )