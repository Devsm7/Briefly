"""
Backfill script: re-translate summary_ar for all articles where language='ar'.
Runs the new Groq-based translate_to_arabic() against the existing English summary.

Usage (inside container):
    python scripts/retranslate_arabic.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
from openai import RateLimitError

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.news import News
from app.services.summarizer import _groq_client, _GROQ_MODEL

def translate_with_retry(text: str, retries: int = 5) -> str | None:
    client = _groq_client()
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=_GROQ_MODEL,
                messages=[{
                    "role": "user",
                    "content": (
                        "Translate the following text to Arabic. "
                        "Output Arabic words only — no English, no transliteration, no explanations.\n\n"
                        f"{text[:1500]}"
                    ),
                }],
                temperature=0.1,
                max_tokens=600,
            )
            return (resp.choices[0].message.content or "").strip() or None
        except RateLimitError:
            wait = 10 * (attempt + 1)
            print(f"    Rate limited, waiting {wait}s…")
            time.sleep(wait)
        except Exception as exc:
            print(f"    Error: {exc}")
            return None
    return None

db = SessionLocal()
try:
    articles = db.query(News).filter(
        News.language == "ar",
        News.summary.isnot(None),
    ).all()

    print(f"Found {len(articles)} Arabic articles to retranslate.")
    updated = skipped = failed = 0

    for i, article in enumerate(articles, 1):
        ar = translate_with_retry(article.summary)
        if ar:
            article.summary_ar = ar
            updated += 1
        else:
            failed += 1

        time.sleep(8)  # 600 tokens/call × 7.5 calls/min = ~4500 TPM, under 8000 limit

        if i % 10 == 0:
            db.commit()
            print(f"  {i}/{len(articles)} — updated={updated} failed={failed}")

    db.commit()
    print(f"\nDone: updated={updated} skipped={skipped} failed={failed}")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
    raise
finally:
    db.close()
