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
        success = 0
        for i, a in enumerate(articles, 1):
            print(f"[{i}/{total}] {a.title[:60]}...")
            summary = generate_summary(a.content, a.title)
            if summary:
                # Update in a fresh session to avoid stale connection
                db2 = SessionLocal()
                try:
                    article = db2.query(News).get(a.article_id)
                    article.summary = summary
                    db2.commit()
                    success += 1
                    print(f"  OK: {summary[:80]}...")
                finally:
                    db2.close()
            else:
                print("  FAILED")
            if i % 10 == 0:
                print(f"-- Progress: {i}/{total} ({success} ok) --")
    finally:
        db.close()
    print(f"Done. {success}/{total} articles summarized.")


if __name__ == "__main__":
    main()
