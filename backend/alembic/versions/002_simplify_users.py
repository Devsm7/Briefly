"""simplify users: remove email/password, add first_name/last_name/gender

Revision ID: 002
Revises: 001
Create Date: 2026-04-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns
    op.add_column('users', sa.Column('first_name', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('gender', sa.String(20), nullable=True))

    # Populate first_name/last_name from full_name where possible
    op.execute("""
        UPDATE users SET
            first_name = COALESCE(split_part(full_name, ' ', 1), username),
            last_name  = COALESCE(NULLIF(split_part(full_name, ' ', 2), ''), '-')
    """)

    # Make first_name/last_name NOT NULL
    op.alter_column('users', 'first_name', nullable=False)
    op.alter_column('users', 'last_name', nullable=False)

    # Drop old columns
    op.drop_column('users', 'email')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'full_name')
    op.drop_column('users', 'reset_token')
    op.drop_column('users', 'reset_token_expires')


def downgrade() -> None:
    # Re-add dropped columns
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('hashed_password', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('full_name', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('reset_token', sa.String(64), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(timezone=True), nullable=True))

    # Merge first_name + last_name back to full_name
    op.execute("UPDATE users SET full_name = first_name || ' ' || last_name")

    # Drop new columns
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'gender')
