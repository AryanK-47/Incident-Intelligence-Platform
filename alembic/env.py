from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool

from app.core.database import Base, engine

from app.features.users.models import User
from app.features.roles.models import Role
from app.features.user_roles.models import UserRole
from app.features.comments.models import Comment
from app.features.ai_analysis.models import AiAnalysis
from app.features.Incident.models import Incident
from app.features.Incident_Events.models import Incident_Events
from app.features.Incident.models import Incident
from app.features.Incident_Assignee.models import IncidentAssignee


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()