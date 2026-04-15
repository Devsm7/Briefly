"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-04-05

"""
from typing import Sequence, Union

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tables were created manually via SQL Editor in Neon.
    pass


def downgrade() -> None:
    pass
