from __future__ import annotations

import uuid
from sqlalchemy import DateTime
from app.core.database import Base
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.features.comments.models import Comment
    from app.features.user_roles.models import UserRole


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
        nullable=False
        )
    
    password_hash : Mapped[str] = mapped_column(nullable=False)

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    
    deleted_at : Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None
    )

    user_roles : Mapped[list["UserRole"]] = relationship(
        back_populates="user",
        cascade= "all, delete-orphan"
    )

    comments : Mapped[list["Comment"]] = relationship(
        back_populates="user"
    )