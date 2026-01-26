"""add runs table

Revision ID: 586a9f6c70f5
Revises: 305f7c1df96a
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "586a9f6c70f5"
down_revision: Union[str, None] = "305f7c1df96a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "entity_id", sa.Integer(), sa.ForeignKey("entities.id"), nullable=False
        ),
        sa.Column(
            "period_id", sa.Integer(), sa.ForeignKey("periods.id"), nullable=False
        ),
        sa.Column(
            "config_version_id",
            sa.Integer(),
            sa.ForeignKey("config_versions.id"),
            nullable=False,
        ),
        sa.Column("run_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), default="draft"),
        sa.Column("inputs_hash", sa.String(64)),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now()),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("approved_at", sa.DateTime()),
        sa.Column("approved_by", sa.Integer(), sa.ForeignKey("users.id")),
        sa.UniqueConstraint("period_id", "run_number", name="uq_period_run"),
    )


def downgrade() -> None:
    op.drop_table("runs")
