"""Translation endpoint — translates English AI summaries to Arabic via Ollama."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.summarizer import translate_to_arabic

router = APIRouter(prefix="/translate", tags=["translate"])


class TranslateRequest(BaseModel):
    text: str


class TranslateResponse(BaseModel):
    translated: str | None


@router.post("", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    return TranslateResponse(translated=translate_to_arabic(req.text))
