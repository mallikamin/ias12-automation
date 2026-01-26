"""add tax_rates table

Revision ID: bdc62754e3ff
Revises: dc1d490f1d3a
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "bdc62754e3ff"
down_revision: Union[str, None] = "dc1d490f1d3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tax_rates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "entity_id", sa.Integer(), sa.ForeignKey("entities.id"), nullable=False
        ),
        sa.Column("effective_date", sa.String(10), nullable=False),
        sa.Column("rate", sa.Numeric(5, 2), nullable=False),
        sa.Column("surtax_rate", sa.Numeric(5, 2), default=0),
        sa.Column("description", sa.String(255)),
        sa.Column("is_enacted", sa.Integer(), default=1),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now()),
        sa.UniqueConstraint("entity_id", "effective_date", name="uq_entity_rate_date"),
    )


def downgrade() -> None:
    op.drop_table("tax_rates")
