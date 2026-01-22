"""add account_mappings table

Revision ID: dc1d490f1d3a
Revises: 90a7a7d12083
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "dc1d490f1d3a"
down_revision: Union[str, None] = "90a7a7d12083"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "account_mappings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "entity_id", sa.Integer(), sa.ForeignKey("entities.id"), nullable=False
        ),
        sa.Column("account_code", sa.String(50), nullable=False),
        sa.Column("tax_category", sa.String(50), nullable=False),
        sa.Column("tax_base_rule", sa.String(50), nullable=False),
        sa.Column("deductibility", sa.String(50), nullable=False),
        sa.Column("posting_route", sa.String(20), nullable=False),
        sa.Column("description", sa.String(255)),
        sa.Column("is_active", sa.Integer(), default=1),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime()),
        sa.Column("updated_by", sa.Integer(), sa.ForeignKey("users.id")),
        sa.UniqueConstraint("entity_id", "account_code", name="uq_entity_mapping"),
    )


def downgrade() -> None:
    op.drop_table("account_mappings")
