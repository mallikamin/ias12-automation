"""add source_files and source_rows tables

Revision ID: b73194f0d95b
Revises: 77ba7a1471e6
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b73194f0d95b"
down_revision: Union[str, None] = "77ba7a1471e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "source_files",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "entity_id", sa.Integer(), sa.ForeignKey("entities.id"), nullable=False
        ),
        sa.Column(
            "period_id", sa.Integer(), sa.ForeignKey("periods.id"), nullable=False
        ),
        sa.Column("file_type", sa.String(50), nullable=False),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_hash", sa.String(64)),
        sa.Column("row_count", sa.Integer()),
        sa.Column("uploaded_by", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("uploaded_at", sa.DateTime(), default=sa.func.now()),
    )

    op.create_table(
        "source_rows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "source_file_id",
            sa.Integer(),
            sa.ForeignKey("source_files.id"),
            nullable=False,
        ),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(50)),
        sa.Column("account_name", sa.String(255)),
        sa.Column("balance", sa.Numeric(18, 2)),
        sa.Column("additional_data", sa.Text()),
    )


def downgrade() -> None:
    op.drop_table("source_rows")
    op.drop_table("source_files")
