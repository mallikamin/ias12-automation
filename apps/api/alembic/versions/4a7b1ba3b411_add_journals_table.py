"""add journals table

Revision ID: 4a7b1ba3b411
Revises: 7b44441d718e
Create Date: 2026-01-26 20:22:36.942285

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4a7b1ba3b411"
down_revision: Union[str, None] = "7b44441d718e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "journals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("runs.id"), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(50), nullable=False),
        sa.Column("account_name", sa.String(255)),
        sa.Column("debit", sa.Numeric(18, 2), default=0),
        sa.Column("credit", sa.Numeric(18, 2), default=0),
        sa.Column("posting_route", sa.String(20), nullable=False),
        sa.Column("description", sa.String(255)),
        sa.Column("register_line_ids", sa.Text()),
    )


def downgrade() -> None:
    op.drop_table("journals")
