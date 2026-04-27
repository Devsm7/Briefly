"""Ollama-powered article summarization."""

import json
import logging
import subprocess

logger = logging.getLogger(__name__)

_SUMMARY_TIMEOUT = 240  # seconds


def generate_summary(content: str | None, title: str, retries: int = 2) -> str | None:
    """
    Generate a 2-3 sentence summary of an article using Ollama mistral.

    Args:
        content: The article body text (may be None or short).
        title: The article title, used as context.

    Returns:
        The generated summary string, or None if summarization failed.
    """
    if not content or len(content) < 50:
        return None

    # Truncate to avoid excessively long prompts (Ollama context limits vary)
    truncated = content[:4000]

    prompt = f"""Summarize this article in 2-3 concise sentences.
Give the reader a clear sense of what the article is about without editorializing.

Title: {title}

Article:
{truncated}

Summary:"""

    for attempt in range(retries + 1):
        try:
            result = subprocess.run(
                [
                    "curl", "-s", "--max-time", str(_SUMMARY_TIMEOUT),
                    "-X", "POST", "http://localhost:11434/api/generate",
                    "-d", json.dumps({
                        "model": "mistral",
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.3, "num_predict": 256},
                    }),
                ],
                capture_output=True,
                text=True,
                timeout=_SUMMARY_TIMEOUT + 15,
            )
            if result.returncode != 0:
                logger.warning("Ollama curl failed (returncode=%d, stderr=%r)", result.returncode, result.stderr)
                if attempt == retries:
                    return None
                continue
            data = json.loads(result.stdout)
            summary = (data.get("response") or "").strip()
            if summary:
                logger.debug("Generated summary (%d chars) for title: %s", len(summary), title)
                return summary
            if attempt == retries:
                return None
        except subprocess.TimeoutExpired as exc:
            logger.warning("Ollama summarization timed out after %ds", _SUMMARY_TIMEOUT)
            if attempt == retries:
                return None
        except Exception as exc:
            logger.warning("Unexpected error during summarization: %s", exc)
            if attempt == retries:
                return None
