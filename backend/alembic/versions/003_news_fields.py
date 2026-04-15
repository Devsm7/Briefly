"""Add newsdata_id, content, keywords, author, embedding to news table

Revision ID: 003
Revises: 002
Create Date: 2026-04-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # newsdata_id — dedup key from NewsData.io API (their `article_id` field)
    op.add_column("news", sa.Column("newsdata_id", sa.String(100), nullable=True))
    op.create_index("ix_news_newsdata_id", "news", ["newsdata_id"], unique=True)

    # content — full article text (may be null on free tier)
    op.add_column("news", sa.Column("content", sa.Text(), nullable=True))

    # keywords — array of keyword strings from NewsData
    op.add_column("news", sa.Column("keywords", ARRAY(sa.String()), nullable=True))

    # author — joined creator list from NewsData
    op.add_column("news", sa.Column("author", sa.String(255), nullable=True))

    # embedding — 384-dim sentence-transformer vector (populated by embedding job)
    op.add_column("news", sa.Column("embedding", ARRAY(sa.Float()), nullable=True))


def downgrade() -> None:
    op.drop_index("ix_news_newsdata_id", table_name="news")
    op.drop_column("news", "newsdata_id")
    op.drop_column("news", "content")
    op.drop_column("news", "keywords")
    op.drop_column("news", "author")
    op.drop_column("news", "embedding")
