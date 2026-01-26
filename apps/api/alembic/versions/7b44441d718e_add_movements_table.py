"""add movements table

Revision ID: 7b44441d718e
Revises: 68f7c71fff66
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "7b44441d718e"
down_revision: Union[str, None] = "68f7c71fff66"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("runs.id"), nullable=False),
        sa.Column("tax_category", sa.String(50), nullable=False),
        sa.Column("opening_balance", sa.Numeric(18, 2), default=0),
        sa.Column("charged_to_pnl", sa.Numeric(18, 2), default=0),
        sa.Column("charged_to_oci", sa.Numeric(18, 2), default=0),
        sa.Column("charged_to_equity", sa.Numeric(18, 2), default=0),
        sa.Column("acquisitions", sa.Numeric(18, 2), default=0),
        sa.Column("disposals", sa.Numeric(18, 2), default=0),
        sa.Column("fx_movement", sa.Numeric(18, 2), default=0),
        sa.Column("rate_change_impact", sa.Numeric(18, 2), default=0),
        sa.Column("other_adjustments", sa.Numeric(18, 2), default=0),
        sa.Column("closing_balance", sa.Numeric(18, 2), default=0),
    )


def downgrade() -> None:
    op.drop_table("movements")
