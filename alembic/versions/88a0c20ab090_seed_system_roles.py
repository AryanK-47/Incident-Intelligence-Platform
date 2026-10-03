"""seed system roles

Revision ID: 88a0c20ab090
Revises: 81e845fa54f0
Create Date: 2026-09-28 12:24:14.327981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88a0c20ab090'
down_revision: Union[str, Sequence[str], None] = '81e845fa54f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
                INSERT INTO roles(id,name)
                VALUES
                        (gen_random_uuid(),'ADMIN'),
                        (gen_random_uuid(), 'VIEWER')
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
                DELETE FROM roles
                WHERE name IN ('ADMIN','VIEWER')
    """)
