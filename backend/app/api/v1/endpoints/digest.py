"""Daily AI digest endpoints."""

# TODO: Import APIRouter, Depends from fastapi
# TODO: Import get_current_user, get_db, digest_builder

router = None  # TODO: router = APIRouter(prefix="/digest", tags=["digest"])


def get_today_digest():
    """
    GET /digest/today
    Return the current user's AI-generated daily digest.
    - Covers all subscribed categories
    - Each section has 3-5 bullet summaries
    - Includes source attribution and links
    - Generated once per day and cached; regenerated if stale
    """
    # TODO: implement
    raise NotImplementedError


def regenerate_digest():
    """
    POST /digest/regenerate
    Force-regenerate the user's digest using the latest articles.
    """
    # TODO: implement
    raise NotImplementedError
