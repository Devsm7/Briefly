"""Batch embedding script — run via: python scripts/batch_embed.py"""

import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


from app.db.session import SessionLocal
from app.models.news import News
from app.recommender.embedder import embedder

def main():
    db = SessionLocal()
    try:
        articles = db.query(News).filter(
            News.embedding == None,
            News.summary != None
        ).all()
        total = len(articles)
        print(f"found {total} articles without embeddings")

        for i in range(0,total,32):
            batch = articles[i:i+32]
            texts = [a.summary for a in batch]
            vectors = embedder.embed_batch(texts)
            for article,vec in zip(batch, vectors):
                article.embedding = vec
            db.commit()
            print(f"-- Embedded {min(i + 32, total)}/{total} --")

    finally:
        db.close()
    print(f"Done. {total} articles embedded.")
if __name__ == "__main__":
    main()
