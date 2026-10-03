from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.features.users.models import User
    from app.features.roles.models import Role

class UserRole(Base):
    __tablename__ = "user_roles"
    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key = True
    )
    role_id  : Mapped[uuid.UUID] = mapped_column(
        ForeignKey ("roles.id"),
        primary_key=True
    )
    user : Mapped["User"] = relationship(
        back_populates = "user_roles"
    )
    role : Mapped["Role"] = relationship(
        back_populates = "user_roles"
    )


