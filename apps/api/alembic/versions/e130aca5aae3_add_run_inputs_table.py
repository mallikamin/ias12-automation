"""add run_inputs table

Revision ID: e130aca5aae3
Revises: 586a9f6c70f5
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "e130aca5aae3"
down_revision: Union[str, None] = "586a9f6c70f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "run_inputs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("runs.id"), nullable=False),
        sa.Column(
            "source_file_id",
            sa.Integer(),
            sa.ForeignKey("source_files.id"),
            nullable=False,
        ),
        sa.Column("file_hash", sa.String(64), nullable=False),
        sa.UniqueConstraint("run_id", "source_file_id", name="uq_run_source"),
    )


def downgrade() -> None:
    op.drop_table("run_inputs")
