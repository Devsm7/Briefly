"""REST API client — single module for all backend HTTP calls from Streamlit pages."""

import os
import requests
import streamlit as st

BASE_URL = os.getenv("BACKEND_URL", "http://localhost")
_TIMEOUT = 15


def _auth() -> dict:
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _handle(response: requests.Response) -> dict | list:
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        if response.content:
            try:
                detail = response.json().get("detail", str(exc))
            except Exception:
                detail = response.text[:200] or str(exc)
        else:
            detail = str(exc)
        raise RuntimeError(detail) from exc
    try:
        return response.json()
    except Exception as exc:
        raise RuntimeError(
            f"Server returned status {response.status_code} but non-JSON body: {response.text[:200]}"
        ) from exc


# ── Auth ─────────────────────────────────────────────────────────────────────

def login(username: str) -> dict:
    return _handle(requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"username": username},
        timeout=_TIMEOUT,
    ))


def register(username: str, first_name: str, last_name: str, gender: str) -> dict:
    return _handle(requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={"username": username, "first_name": first_name,
              "last_name": last_name, "gender": gender},
        timeout=_TIMEOUT,
    ))


# ── User ──────────────────────────────────────────────────────────────────────

def get_me() -> dict:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/users/me",
        headers=_auth(),
        timeout=_TIMEOUT,
    ))


def get_me_with_survey() -> dict:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/users/me/with-survey",
        headers=_auth(),
        timeout=_TIMEOUT,
    ))


# ── Survey ────────────────────────────────────────────────────────────────────

def has_completed_survey() -> bool:
    """Check if the current user has completed the onboarding survey."""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/survey",
            headers=_auth(),
            timeout=_TIMEOUT,
        )
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
    except requests.exceptions.ConnectionError:
        # Backend not running — assume no survey to avoid blocking the UI
        return False
    except RuntimeError as e:
        err_str = str(e)
        if "Not authenticated" in err_str or "403" in err_str:
            # Auth is broken — clear session and redirect to login
            st.session_state.clear()
            st.switch_page("pages/log_in_page.py")
            st.stop()
        raise


def submit_survey(categories: list, answers: dict) -> dict:
    try:
        return _handle(requests.post(
            f"{BASE_URL}/api/v1/survey",
            json={"categories": categories, "answers": answers},
            headers=_auth(),
            timeout=_TIMEOUT,
        ))
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError("Backend is not running. Please start the server and try again.") from exc


def skip_survey() -> dict:
    try:
        return _handle(requests.post(
            f"{BASE_URL}/api/v1/survey/skip",
            headers=_auth(),
            timeout=_TIMEOUT,
        ))
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError("Backend is not running. Please start the server and try again.") from exc


# ── News ─────────────────────────────────────────────────────────────────────

def get_news(page: int = 1, per_page: int = 50) -> dict:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/news",
        params={"page": page, "per_page": per_page},
        timeout=_TIMEOUT,
    ))


def get_recommendations(page: int = 1, per_page: int = 50) -> dict:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/recommendations",
        params={"page": page, "per_page": per_page},
        headers=_auth(),
        timeout=60,
    ))


def translate_summary(text: str) -> str | None:
    try:
        data = _handle(requests.post(
            f"{BASE_URL}/api/v1/translate",
            json={"text": text},
            timeout=60,
        ))
        return data.get("translated")
    except Exception:
        return None


def get_article(article_id: int) -> dict:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/news/{article_id}",
        timeout=_TIMEOUT,
    ))


def get_library() -> list:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/news/library",
        headers=_auth(),
        timeout=_TIMEOUT,
    ))


def save_article(article_id: int) -> None:
    _handle(requests.post(
        f"{BASE_URL}/api/v1/news/save/{article_id}",
        headers=_auth(),
        timeout=_TIMEOUT,
    ))


def unsave_article(article_id: int) -> None:
    _handle(requests.delete(
        f"{BASE_URL}/api/v1/news/save/{article_id}",
        headers=_auth(),
        timeout=_TIMEOUT,
    ))


def check_saved(article_id: int) -> bool:
    try:
        data = _handle(requests.get(
            f"{BASE_URL}/api/v1/news/saved/{article_id}",
            headers=_auth(),
            timeout=_TIMEOUT,
        ))
        return data.get("saved", False)
    except Exception:
        return False


# ── Search ────────────────────────────────────────────────────────────────────

def search_articles(q: str, category: str | None = None, limit: int = 10) -> list:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/news/search",
        params={"q": q, "category": category, "limit": limit},
        timeout=_TIMEOUT,
    ))


# ── Category Digests ────────────────────────────────────────────────────────────

def get_overall_summary() -> str:
    data = _handle(requests.get(
        f"{BASE_URL}/api/v1/news/overall",
        headers=_auth(),
        timeout=300,
    ))
    return data.get("summary", "")


def get_category_digests() -> dict:
    return _handle(requests.get(
        f"{BASE_URL}/api/v1/news/digest",
        timeout=_TIMEOUT,
    ))
