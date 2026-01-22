"""add entities and periods tables

Revision ID: 77ba7a1471e6
Revises: 083f0729c6ab
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "77ba7a1471e6"
down_revision: Union[str, None] = "083f0729c6ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Entities table
    op.create_table(
        "entities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("jurisdiction", sa.String(100), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("tax_authority", sa.String(100)),
        sa.Column("fiscal_year_end", sa.String(5), nullable=False),
        sa.Column("is_active", sa.Integer(), default=1),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now()),
    )

    # Periods table
    op.create_table(
        "periods",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "entity_id", sa.Integer(), sa.ForeignKey("entities.id"), nullable=False
        ),
        sa.Column("period_end", sa.String(10), nullable=False),
        sa.Column("period_name", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), default="open"),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now()),
        sa.Column("locked_at", sa.DateTime(), nullable=True),
        sa.Column("locked_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("periods")
    op.drop_table("entities")
