"""Add summary_ar column for Arabic translation of AI summary

Revision ID: 006
Revises: 005
Create Date: 2026-05-10
"""

import sqlalchemy as sa
from alembic import op

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("news", sa.Column("summary_ar", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("news", "summary_ar")
