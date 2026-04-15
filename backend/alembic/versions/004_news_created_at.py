"""Add created_at column to news table

Revision ID: 004
Revises: 003
Create Date: 2026-04-15
"""

import sqlalchemy as sa
from alembic import op

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "news",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("news", "created_at")
