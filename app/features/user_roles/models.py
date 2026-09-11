from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
import uuid

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

