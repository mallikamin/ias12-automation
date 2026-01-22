"""create users roles audit_log tables

Revision ID: 083f0729c6ab
Revises:
Create Date: 2026-01-22 15:01:53.343883
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "083f0729c6ab"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Roles table
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(50), unique=True, nullable=False),
        sa.Column("description", sa.String(255)),
    )

    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("is_active", sa.Integer(), default=1),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now()),
    )

    # Audit log table
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("table_name", sa.String(100), nullable=False),
        sa.Column("record_id", sa.Integer()),
        sa.Column("old_values", sa.Text()),
        sa.Column("new_values", sa.Text()),
        sa.Column("reason", sa.String(500)),
        sa.Column("timestamp", sa.DateTime(), default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("audit_log")
    op.drop_table("users")
    op.drop_table("roles")
