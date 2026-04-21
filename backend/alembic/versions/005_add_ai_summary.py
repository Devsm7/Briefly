"""Add ai_summary column to news table

Revision ID: 005
Revises: 004
Create Date: 2026-04-21
"""

import sqlalchemy as sa
from alembic import op

revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "news",
        sa.Column(
            "ai_summary",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("news", "ai_summary")