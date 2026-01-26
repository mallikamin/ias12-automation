"""add config_versions table

Revision ID: 305f7c1df96a
Revises: bdc62754e3ff
Create Date: 2026-01-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "305f7c1df96a"
down_revision: Union[str, None] = "bdc62754e3ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "config_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "entity_id", sa.Integer(), sa.ForeignKey("entities.id"), nullable=False
        ),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(255)),
        sa.Column("mappings_hash", sa.String(64)),
        sa.Column("rates_hash", sa.String(64)),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now()),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id")),
        sa.UniqueConstraint("entity_id", "version_number", name="uq_entity_version"),
    )


def downgrade() -> None:
    op.drop_table("config_versions")
