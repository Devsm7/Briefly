"""AI news agent endpoint — /api/v1/agent"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import decode_token
from app.models.user import User
from app.services.agent_service import run_agent

router = APIRouter(prefix="/agent", tags=["agent"])

_optional_bearer = HTTPBearer(auto_error=False)


def _optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_optional_bearer),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Return the current user if a valid token is present, otherwise None."""
    if credentials is None:
        return None
    payload = decode_token(credentials.credentials)
    if payload is None:
        return None
    user_id = payload.get("sub")
    if user_id is None:
        return None
    return db.query(User).filter(User.id == int(user_id), User.is_active == True).first()


class ConversationMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class AgentRequest(BaseModel):
    message: str
    conversation_history: Optional[list[ConversationMessage]] = []


class AgentResponse(BaseModel):
    response: str
    usage: Optional[dict] = None


@router.post("", response_model=AgentResponse)
def chat(
    body: AgentRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(_optional_user),
):
    """
    Chat with the Briefly AI news agent.

    Supports article search, Q&A, and summaries without authentication.
    Personalized recommendations require a Bearer token.
    """
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI agent unavailable — ANTHROPIC_API_KEY not configured.",
        )

    history = [
        {"role": m.role, "content": m.content}
        for m in (body.conversation_history or [])
    ]

    result = run_agent(
        message=body.message,
        db=db,
        api_key=settings.ANTHROPIC_API_KEY,
        user_id=current_user.id if current_user else None,
        conversation_history=history,
    )

    return AgentResponse(response=result["response"], usage=result.get("usage"))
