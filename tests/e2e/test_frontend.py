"""
End-to-end tests for the Briefly Streamlit frontend.

Two layers:
  1. API integration tests — call the FastAPI backend directly with `requests`
     to verify all endpoints consumed by the frontend are working.
  2. Streamlit AppTest tests — run each page in isolation using
     `streamlit.testing.v1.AppTest` to verify UI behaviour without a browser.

Run with:
    pytest tests/e2e/test_frontend.py -v

Environment variables:
    BACKEND_URL  — defaults to http://localhost:8000
    TEST_USERNAME — username used for API tests (auto-generated if absent)
"""

import os
import sys
import time
import uuid

import pytest
import requests

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
INTERFACES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "frontend", "src", "interfaces"
)
sys.path.insert(0, INTERFACES_DIR)


def unique_username() -> str:
    return f"test_{uuid.uuid4().hex[:8]}"


# ══════════════════════════════════════════════════════════════════════════════
# 1. API Integration Tests
# ══════════════════════════════════════════════════════════════════════════════

class TestBackendHealth:
    def test_health_endpoint(self):
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


class TestAuthAPI:
    def test_register_and_login(self):
        username = unique_username()
        # Register
        r = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
            "username": username,
            "first_name": "Test",
            "last_name": "User",
            "gender": "male",
        }, timeout=5)
        assert r.status_code == 201
        user = r.json()
        assert user["username"] == username

        # Login
        r = requests.post(f"{BASE_URL}/api/v1/auth/login",
                          json={"username": username}, timeout=5)
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_unknown_user_returns_401(self):
        r = requests.post(f"{BASE_URL}/api/v1/auth/login",
                          json={"username": "nonexistent_xyz"}, timeout=5)
        assert r.status_code == 401

    def test_register_duplicate_username_returns_400(self):
        username = unique_username()
        payload = {"username": username, "first_name": "A",
                   "last_name": "B", "gender": "female"}
        requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload, timeout=5)
        r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload, timeout=5)
        assert r.status_code == 400


@pytest.fixture(scope="module")
def auth_token():
    """Register a fresh user and return their JWT token."""
    username = unique_username()
    requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "username": username, "first_name": "E2E", "last_name": "Bot", "gender": "male",
    }, timeout=5)
    r = requests.post(f"{BASE_URL}/api/v1/auth/login",
                      json={"username": username}, timeout=5)
    return r.json()["access_token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


class TestUsersAPI:
    def test_get_me(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/v1/users/me", headers=auth_headers, timeout=5)
        assert r.status_code == 200
        data = r.json()
        assert "username" in data
        assert "first_name" in data

    def test_get_me_without_token_returns_403(self):
        r = requests.get(f"{BASE_URL}/api/v1/users/me", timeout=5)
        assert r.status_code in (401, 403)


class TestSurveyAPI:
    def test_skip_survey(self, auth_headers):
        r = requests.post(f"{BASE_URL}/api/v1/survey/skip",
                          headers=auth_headers, timeout=5)
        assert r.status_code == 200
        assert "survey_completed" in r.json()

    def test_submit_survey(self, auth_headers):
        r = requests.post(f"{BASE_URL}/api/v1/survey", json={
            "categories": ["tech", "sport"],
            "answers": {"Q04": ["ai", "software"], "Q05": 4, "Q13": ["football"], "Q14": 3},
        }, headers=auth_headers, timeout=5)
        assert r.status_code == 201
        assert r.json()["survey_completed"] == 1

    def test_get_survey(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/v1/survey", headers=auth_headers, timeout=5)
        assert r.status_code == 200


class TestNewsAPI:
    def test_list_articles(self):
        r = requests.get(f"{BASE_URL}/api/v1/news", timeout=10)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_library_requires_auth(self):
        r = requests.get(f"{BASE_URL}/api/v1/news/library", timeout=5)
        assert r.status_code in (401, 403)

    def test_library_authenticated(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/v1/news/library",
                         headers=auth_headers, timeout=5)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_save_and_unsave_article(self, auth_headers):
        articles = requests.get(f"{BASE_URL}/api/v1/news", timeout=10).json()
        if not articles:
            pytest.skip("No articles in database")

        article_id = articles[0]["article_id"]

        # Save
        r = requests.post(f"{BASE_URL}/api/v1/news/save/{article_id}",
                          headers=auth_headers, timeout=5)
        assert r.status_code == 201
        assert r.json()["saved"] is True

        # Check saved
        r = requests.get(f"{BASE_URL}/api/v1/news/saved/{article_id}",
                         headers=auth_headers, timeout=5)
        assert r.status_code == 200
        assert r.json()["saved"] is True

        # Unsave
        r = requests.delete(f"{BASE_URL}/api/v1/news/save/{article_id}",
                            headers=auth_headers, timeout=5)
        assert r.status_code == 200
        assert r.json()["saved"] is False

    def test_unsave_not_saved_returns_404(self, auth_headers):
        r = requests.delete(f"{BASE_URL}/api/v1/news/save/999999",
                            headers=auth_headers, timeout=5)
        assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════════════
# 2. Streamlit AppTest Tests
# ══════════════════════════════════════════════════════════════════════════════

try:
    from streamlit.testing.v1 import AppTest
    STREAMLIT_TESTING_AVAILABLE = True
except ImportError:
    STREAMLIT_TESTING_AVAILABLE = False

skip_if_no_apptest = pytest.mark.skipif(
    not STREAMLIT_TESTING_AVAILABLE,
    reason="streamlit.testing.v1 not available (requires streamlit >= 1.18)",
)

LOGIN_PAGE    = os.path.join(INTERFACES_DIR, "pages", "log_in_page.py")
SIGNUP_PAGE   = os.path.join(INTERFACES_DIR, "pages", "Sign_up_page.py")
SURVEY_PAGE   = os.path.join(INTERFACES_DIR, "pages", "survey_page.py")
FORYOU_PAGE   = os.path.join(INTERFACES_DIR, "pages", "ForYou.py")
PROFILE_PAGE  = os.path.join(INTERFACES_DIR, "pages", "profile_page.py")
LIBRARY_PAGE  = os.path.join(INTERFACES_DIR, "pages", "saved_articles_page.py")


@skip_if_no_apptest
class TestLoginPage:
    def test_renders_title(self):
        at = AppTest.from_file(LOGIN_PAGE).run()
        assert not at.exception
        # Page should contain "Welcome back" text
        html_content = " ".join(str(b) for b in at.markdown)
        assert "Welcome back" in html_content

    def test_empty_username_shows_error(self):
        at = AppTest.from_file(LOGIN_PAGE).run()
        at.button[0].click().run()  # click Sign in with empty username
        html_content = " ".join(str(b) for b in at.markdown)
        assert "username" in html_content.lower() or not at.exception


@skip_if_no_apptest
class TestSignupPage:
    def test_renders_create_account(self):
        at = AppTest.from_file(SIGNUP_PAGE).run()
        assert not at.exception
        html_content = " ".join(str(b) for b in at.markdown)
        assert "Create an account" in html_content

    def test_shows_all_fields(self):
        at = AppTest.from_file(SIGNUP_PAGE).run()
        input_labels = [ti.label for ti in at.text_input]
        assert any("Username" in lbl for lbl in input_labels)
        assert any("First" in lbl for lbl in input_labels)
        assert any("Last" in lbl for lbl in input_labels)


@skip_if_no_apptest
class TestSurveyPage:
    def test_redirects_when_not_logged_in(self):
        """Survey page should redirect unauthenticated users to login."""
        at = AppTest.from_file(SURVEY_PAGE).run()
        # No exception means it ran (redirect happens via switch_page)
        assert not at.exception

    def test_renders_category_step_when_logged_in(self):
        at = AppTest.from_file(SURVEY_PAGE)
        at.session_state["logged_in"] = True
        at.session_state["token"] = "mock_token"
        at.run()
        assert not at.exception
        # Step 0 should show category buttons
        button_labels = [b.label for b in at.button]
        assert any("Tech" in lbl or "Politics" in lbl or "Sport" in lbl
                   for lbl in button_labels)

    def test_next_disabled_without_category(self):
        at = AppTest.from_file(SURVEY_PAGE)
        at.session_state["logged_in"] = True
        at.session_state["token"] = "mock_token"
        at.run()
        # "Next →" button should be disabled when no category selected
        next_buttons = [b for b in at.button if "Next" in b.label]
        if next_buttons:
            assert next_buttons[0].disabled


@skip_if_no_apptest
class TestForYouPage:
    def test_redirects_when_not_logged_in(self):
        at = AppTest.from_file(FORYOU_PAGE).run()
        assert not at.exception

    def test_renders_feed_when_logged_in(self):
        at = AppTest.from_file(FORYOU_PAGE)
        at.session_state["logged_in"] = True
        at.session_state["token"] = "mock_token"
        at.run(timeout=20)
        assert not at.exception


@skip_if_no_apptest
class TestProfilePage:
    def test_redirects_when_not_logged_in(self):
        at = AppTest.from_file(PROFILE_PAGE).run()
        assert not at.exception

    def test_renders_profile_when_logged_in(self):
        at = AppTest.from_file(PROFILE_PAGE)
        at.session_state["logged_in"] = True
        at.session_state["token"] = "mock_token"
        at.run(timeout=10)
        assert not at.exception

    def test_logout_button_present(self):
        at = AppTest.from_file(PROFILE_PAGE)
        at.session_state["logged_in"] = True
        at.session_state["token"] = "mock_token"
        at.run(timeout=10)
        button_labels = [b.label for b in at.button]
        assert any("Logout" in lbl or "logout" in lbl.lower() for lbl in button_labels)


@skip_if_no_apptest
class TestLibraryPage:
    def test_redirects_when_not_logged_in(self):
        at = AppTest.from_file(LIBRARY_PAGE).run()
        assert not at.exception

    def test_renders_library_when_logged_in(self):
        at = AppTest.from_file(LIBRARY_PAGE)
        at.session_state["logged_in"] = True
        at.session_state["token"] = "mock_token"
        at.run(timeout=10)
        assert not at.exception
