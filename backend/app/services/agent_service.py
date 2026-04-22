"""Claude-powered news agent with tool use for article search and recommendations."""

import json
from typing import Optional

import anthropic
from sqlalchemy import func as sqlfunc, or_
from sqlalchemy.orm import Session

from ..models.news import News
from ..models.survey import SurveyPreference

SYSTEM_PROMPT = """You are Briefly's AI news assistant. You help users discover, understand, and explore news articles.

When answering questions about news or current events, always use your tools to search for relevant articles first.
When recommending articles, explain why each one matches the user's interests.
Cite article titles and sources in your responses. Be concise and informative."""

_TOOLS = [
    {
        "name": "search_articles",
        "description": "Search news articles by keyword or filter by category. Returns titles, previews, sources, and article IDs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword to match against article titles and descriptions",
                },
                "category": {
                    "type": "string",
                    "description": "Filter by category (e.g. technology, business, sports, health, politics)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (1–10, default 5)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_article_details",
        "description": "Get the full content and AI summary of a specific article by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "article_id": {
                    "type": "integer",
                    "description": "The unique article ID",
                }
            },
            "required": ["article_id"],
        },
    },
    {
        "name": "get_personalized_recommendations",
        "description": "Get news articles personalized to the authenticated user's interests. Requires the user to be logged in.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of recommendations (1–10, default 5)",
                }
            },
            "required": [],
        },
    },
    {
        "name": "get_categories",
        "description": "List all available news categories and the article count in each.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]


# --------------------------------------------------------------------------- #
# Tool implementations                                                          #
# --------------------------------------------------------------------------- #


def _search_articles(db: Session, query: str = None, category: str = None, limit: int = 5) -> str:
    limit = min(max(limit, 1), 10)
    q = db.query(News)

    if query:
        pattern = f"%{query}%"
        q = q.filter(or_(News.title.ilike(pattern), News.description.ilike(pattern)))

    if category:
        q = q.filter(News.category.ilike(f"%{category}%"))

    articles = q.order_by(News.created_at.desc()).limit(limit).all()

    if not articles:
        return json.dumps({"results": [], "message": "No articles found."})

    return json.dumps({
        "results": [
            {
                "article_id": a.article_id,
                "title": a.title,
                "preview": a.ai_summary or a.description or "",
                "category": a.category,
                "source": a.source,
                "published_date": a.published_date,
                "url": a.url,
            }
            for a in articles
        ]
    })


def _get_article_details(db: Session, article_id: int) -> str:
    article = db.query(News).filter(News.article_id == article_id).first()

    if not article:
        return json.dumps({"error": f"Article {article_id} not found."})

    return json.dumps({
        "article_id": article.article_id,
        "title": article.title,
        "ai_summary": article.ai_summary,
        "description": article.description,
        "content": (article.content or "")[:3000],
        "category": article.category,
        "source": article.source,
        "author": article.author,
        "published_date": article.published_date,
        "url": article.url,
    })


def _get_personalized_recommendations(db: Session, user_id: Optional[int], limit: int = 5) -> str:
    if not user_id:
        return json.dumps({"error": "Login required for personalized recommendations."})

    limit = min(max(limit, 1), 10)

    survey = db.query(SurveyPreference).filter(SurveyPreference.user_id == user_id).first()

    if not survey or not survey.interest_vector:
        articles = db.query(News).order_by(News.created_at.desc()).limit(limit).all()
        return json.dumps({
            "message": "No interest profile found — showing recent articles.",
            "results": [
                {
                    "article_id": a.article_id,
                    "title": a.title,
                    "preview": a.ai_summary or a.description or "",
                    "category": a.category,
                    "source": a.source,
                    "url": a.url,
                    "reason": "Recently published",
                }
                for a in articles
            ],
        })

    top_interests = sorted(survey.interest_vector.items(), key=lambda x: x[1], reverse=True)
    results = []
    seen_ids: set[int] = set()

    for category, weight in top_interests:
        if len(results) >= limit:
            break
        articles = (
            db.query(News)
            .filter(News.category.ilike(f"%{category}%"))
            .order_by(News.created_at.desc())
            .limit(limit)
            .all()
        )
        for a in articles:
            if a.article_id not in seen_ids and len(results) < limit:
                seen_ids.add(a.article_id)
                results.append({
                    "article_id": a.article_id,
                    "title": a.title,
                    "preview": a.ai_summary or a.description or "",
                    "category": a.category,
                    "source": a.source,
                    "url": a.url,
                    "reason": f"Matches your interest in {category} ({weight:.0%} relevance)",
                })

    # Pad with recents if needed
    if len(results) < limit:
        extras = (
            db.query(News)
            .filter(News.article_id.notin_(seen_ids) if seen_ids else True)
            .order_by(News.created_at.desc())
            .limit(limit - len(results))
            .all()
        )
        for a in extras:
            results.append({
                "article_id": a.article_id,
                "title": a.title,
                "preview": a.ai_summary or a.description or "",
                "category": a.category,
                "source": a.source,
                "url": a.url,
                "reason": "Recently published",
            })

    return json.dumps({
        "top_interests": dict(top_interests[:3]),
        "results": results,
    })


def _get_categories(db: Session) -> str:
    rows = (
        db.query(News.category, sqlfunc.count(News.article_id).label("count"))
        .filter(News.category.isnot(None))
        .group_by(News.category)
        .order_by(sqlfunc.count(News.article_id).desc())
        .all()
    )
    return json.dumps({
        "categories": [{"name": r.category, "article_count": r.count} for r in rows]
    })


def _execute_tool(name: str, inputs: dict, db: Session, user_id: Optional[int]) -> str:
    if name == "search_articles":
        return _search_articles(db, **inputs)
    if name == "get_article_details":
        return _get_article_details(db, **inputs)
    if name == "get_personalized_recommendations":
        return _get_personalized_recommendations(db, user_id, **inputs)
    if name == "get_categories":
        return _get_categories(db)
    return json.dumps({"error": f"Unknown tool: {name}"})


# --------------------------------------------------------------------------- #
# Public entry point                                                            #
# --------------------------------------------------------------------------- #


def run_agent(
    message: str,
    db: Session,
    api_key: str,
    user_id: Optional[int] = None,
    conversation_history: Optional[list] = None,
) -> dict:
    """Run the news agent and return the final text response."""
    client = anthropic.Anthropic(api_key=api_key)

    messages = list(conversation_history or [])
    messages.append({"role": "user", "content": message})

    while True:
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            text = next(
                (b.text for b in response.content if b.type == "text"),
                "I couldn't generate a response.",
            )
            return {
                "response": text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "cache_read_input_tokens": getattr(response.usage, "cache_read_input_tokens", 0),
                    "cache_creation_input_tokens": getattr(response.usage, "cache_creation_input_tokens", 0),
                },
            }

        if response.stop_reason != "tool_use":
            break

        messages.append({"role": "assistant", "content": response.content})

        tool_results = [
            {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": _execute_tool(block.name, block.input, db, user_id),
            }
            for block in response.content
            if block.type == "tool_use"
        ]
        messages.append({"role": "user", "content": tool_results})

    # Fallback if loop exits unexpectedly
    text = next(
        (b.text for b in response.content if b.type == "text"),
        "I couldn't generate a response.",
    )
    return {"response": text}
