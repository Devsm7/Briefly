"""Batch summarization script — run via: python scripts/batch_summarize.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import SessionLocal
from app.models.news import News
from app.services.summarizer import generate_summary


def main():
    db = SessionLocal()
    try:
        articles = db.query(News).filter(News.summary.is_(None)).all()
        total = len(articles)
        print(f"Found {total} articles without summary")
        for i, a in enumerate(articles, 1):
            print(f"[{i}/{total}] Summarizing: {a.title[:60]}...")
            a.summary = generate_summary(a.content, a.title)
            db.commit()
            if a.summary:
                print(f"  -> {a.summary[:100]}...")
            else:
                print("  -> FAILED (no summary returned)")
    finally:
        db.close()


if __name__ == "__main__":
    main()
