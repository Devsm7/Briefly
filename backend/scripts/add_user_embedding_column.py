"""Migration: add nullable JSONB user_embedding column to survey_preferences."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text(
        "ALTER TABLE survey_preferences ADD COLUMN IF NOT EXISTS user_embedding JSONB"
    ))
    conn.commit()

print("Done — user_embedding column added (or already existed).")
