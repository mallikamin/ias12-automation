"""add chart_of_accounts table

Revision ID: 90a7a7d12083
Revises: b73194f0d95b
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "90a7a7d12083"
down_revision: Union[str, None] = "b73194f0d95b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chart_of_accounts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "entity_id", sa.Integer(), sa.ForeignKey("entities.id"), nullable=False
        ),
        sa.Column("account_code", sa.String(50), nullable=False),
        sa.Column("account_name", sa.String(255), nullable=False),
        sa.Column("account_type", sa.String(50)),
        sa.Column("parent_code", sa.String(50)),
        sa.Column("is_active", sa.Integer(), default=1),
        sa.UniqueConstraint("entity_id", "account_code", name="uq_entity_account"),
    )


def downgrade() -> None:
    op.drop_table("chart_of_accounts")
