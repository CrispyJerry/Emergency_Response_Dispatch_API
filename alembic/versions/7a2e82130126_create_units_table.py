"""create units table

Revision ID: 7a2e82130126
Revises: 
Create Date: 2026-09-24 13:20:42.208744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a2e82130126'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "units",
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("callsign", sa.String(length=20), nullable=False),
        sa.Column("unit_type", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("station_location", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("unit_id", name="units_pkey"),
        sa.UniqueConstraint("callsign", name="units_callsign_key"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("units")
