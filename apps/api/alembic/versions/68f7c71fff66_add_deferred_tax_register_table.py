"""add deferred_tax_register table

Revision ID: 68f7c71fff66
Revises: e130aca5aae3
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "68f7c71fff66"
down_revision: Union[str, None] = "e130aca5aae3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "deferred_tax_register",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("runs.id"), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("source_ref", sa.String(100)),
        sa.Column("tax_category", sa.String(50), nullable=False),
        sa.Column("description", sa.String(255)),
        sa.Column("carrying_amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("tax_base", sa.Numeric(18, 2), nullable=False),
        sa.Column("temporary_difference", sa.Numeric(18, 2), nullable=False),
        sa.Column("tax_rate", sa.Numeric(5, 2), nullable=False),
        sa.Column("deferred_tax_amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("dta_dtl", sa.String(3), nullable=False),
        sa.Column("posting_route", sa.String(20), nullable=False),
        sa.Column("rule_trace", sa.Text()),
    )


def downgrade() -> None:
    op.drop_table("deferred_tax_register")
