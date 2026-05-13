"""
Analyze article summaries in the DB to discover the top 5 topics per category.

Reads real article summaries, asks Groq to identify the most frequently covered
generalized topics, then prints copy-pasteable survey_page.py options + saves JSON.

Usage (inside container):
    docker exec briefly_backend python scripts/discover_topics.py
"""

import json
import os
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.news import News
from openai import OpenAI

_GROQ_MODEL = "llama-3.3-70b-versatile"
_MIN_ARTICLES = 5
_SAMPLE_SIZE = 100
_MAX_TOPICS = 5


def _groq_client() -> OpenAI:
    return OpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )


def _discover_topics(client: OpenAI, category: str, summaries: list[str]) -> list[dict]:
    sample = summaries[:_SAMPLE_SIZE]
    context = "\n".join(f"- {s[:250]}" for s in sample)

    prompt = f"""You are a news analyst. Below are summaries of real news articles in the "{category}" category.
Identify the {_MAX_TOPICS} most frequently covered, distinct thematic topics.

Strict rules:
- NO person names (not "Donald Trump" → use "Presidential Politics" or "Executive Policy")
- NO specific event names (not "Strait of Hormuz Crisis" → use "Maritime Security")
- NO team or league names (not "NFL" → use "American Football"; not "NBA" → use "Basketball")
- NO country names as topics (not "Saudi Arabia" → use "Middle East Affairs")
- Topics must be THEMATIC DOMAINS that will apply to future articles too, not just today's news
- Be specific enough to drive recommendations (e.g. "Cybersecurity" not just "Technology")
- Return ONLY a JSON array of {_MAX_TOPICS} objects, nothing else:
  [{{"label": "Display Name", "code": "snake_case_slug"}}, ...]

Summaries:
{context}

JSON:"""

    try:
        resp = client.chat.completions.create(
            model=_GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300,
        )
        content = (resp.choices[0].message.content or "").strip()
        start = content.find("[")
        end = content.rfind("]") + 1
        if start != -1 and end > start:
            topics = json.loads(content[start:end])
            return [t for t in topics if "label" in t and "code" in t][:_MAX_TOPICS]
    except Exception as exc:
        print(f"  ⚠ Groq error for '{category}': {exc}")
    return []


def main():
    db = SessionLocal()
    try:
        articles = db.query(News).filter(News.summary.isnot(None)).all()
        print(f"Found {len(articles)} articles with summaries\n")

        by_category: dict[str, list[str]] = defaultdict(list)
        for a in articles:
            if a.category:
                by_category[a.category.lower().strip()].append(a.summary)

        # Sort by article count descending
        sorted_cats = sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True)
        print("Categories:")
        for cat, summaries in sorted_cats:
            print(f"  {cat}: {len(summaries)} articles")
        print()

        client = _groq_client()
        results: dict[str, list[dict]] = {}

        for cat, summaries in sorted_cats:
            if len(summaries) < _MIN_ARTICLES:
                print(f"Skipping '{cat}' — only {len(summaries)} articles (min {_MIN_ARTICLES})")
                continue

            print(f"Analyzing '{cat}' ({len(summaries)} articles)…")
            topics = _discover_topics(client, cat, summaries)
            results[cat] = topics
            for t in topics:
                print(f"  ✓ {t['label']} ({t['code']})")
            print()
            time.sleep(1)  # avoid Groq rate limit

    finally:
        db.close()

    # ── Print copy-pasteable survey_page.py format ────────────────────────────
    print("\n" + "=" * 60)
    print("COPY-PASTEABLE survey_page.py OPTIONS")
    print("=" * 60)
    for cat, topics in results.items():
        print(f"\n# {cat}  ({len(by_category[cat])} articles)")
        print(f'        "options": [')
        for t in topics:
            print(f'            ("{t["label"]}", "{t["code"]}"),')
        print("        ],")

    # ── Save JSON ─────────────────────────────────────────────────────────────
    output_path = os.path.join(os.path.dirname(__file__), "discovered_topics.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved to {output_path}")


if __name__ == "__main__":
    main()
