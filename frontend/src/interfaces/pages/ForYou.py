import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

import api_client

st.set_page_config(
    page_title="For You",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if not st.session_state.get("logged_in", False):
    st.warning("Please sign up or log in first.")
    st.switch_page("pages/log_in_page.py")
    st.stop()

# Check if user has completed the onboarding survey
if not api_client.has_completed_survey():
    st.switch_page("pages/survey_page.py")
    st.stop()

st.markdown("""
<style>
    .stApp {
        background: #0b1020;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
        letter-spacing: -0.02em;
    }

    div[data-testid="stImage"] img {
        width: 100%;
        object-fit: cover;
        border-radius: 18px;
        display: block;
    }

    div[data-testid="stButton"] > button {
        min-height: 44px;
        border-radius: 12px;
        font-weight: 600;
    }

    /* يخلي الأعمدة بنفس الارتفاع */
    div[data-testid="column"] {
        display: flex;
    }

    div[data-testid="column"] > div {
        width: 100%;
    }

    /* الكرت نفسه */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #12192b;
        border: 1px solid #1e293b;
        border-radius: 22px;
        padding: 10px;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.18);
    }

    /* المحتوى الداخلي للكرت */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        display: flex;
        flex-direction: column;
    }

    /* Grid - align cards to top, no equal height */
    div[data-testid="stHorizontalBlock"] {
        align-items: start;
    }

    .news-meta {
        color: #91a0b8;
        font-size: 0.82rem;
        margin-top: -0.1rem;
        margin-bottom: 0.55rem;
    }

    .news-preview {
        color: #d8dfeb;
        font-size: 0.97rem;
        line-height: 1.7;
        margin-top: 0.25rem;
        margin-bottom: 0.5rem;
    }

    .ai-label {
        color: #667eea;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .lead-title {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.18;
        margin-top: 0.4rem;
        margin-bottom: 0.6rem;
    }

    .lead-preview {
        color: #d8dfeb;
        font-size: 1.03rem;
        line-height: 1.8;
        margin: 0;
    }

    .lead-ai-label {
        color: #667eea;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .lead-card {
        background: #12192b;
        border: 1px solid #1e293b;
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }

    .card-title {
        color: #f8fafc;
        font-size: 1.22rem;
        font-weight: 760;
        line-height: 1.35;
        margin-top: 0.65rem;
        margin-bottom: 0.55rem;
    }

    .section-label {
        color: #91a0b8;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }

    .top-gap {
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)


def short_preview(text, limit=200):
    if not text:
        return "No preview available."
    text = str(text).strip()
    return text 


def format_meta(article):
    source = article.get("source") or "Unknown source"
    date = article.get("date") or "No date"
    return f"{source} • {date}"


def lead_story(article):
    left, right = st.columns([1.45, 1], gap="medium")

    with left:
        if article.get("cover_image"):
            st.markdown(
                f'<img src="{article["cover_image"]}" style="width:100%;height:430px;object-fit:cover;border-radius:18px;" />',
                unsafe_allow_html=True
            )
        else:
            st.info("No image available")

    with right:
        preview = article.get("preview", "No preview available.")

        st.markdown(f"""
        <div class="lead-card">
            <div class="section-label">Top story</div>
            <div class="lead-title">{article.get("title", "Untitled")}</div>
            <div class="news-meta">{format_meta(article)}</div>
            <div class="lead-ai-label">✨ AI Summary</div>
            <div class="lead-preview">{preview}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Read full story",
            key=f'lead_{article["article_id"]}',
            icon=":material/arrow_forward:",
            use_container_width=True
        ):
            st.switch_page(
                "pages/article_details.py",
                query_params={"article_id": str(article["article_id"])}
            )
            st.stop()


def article_card(article):
    # Card HTML container with visible styling
    st.markdown("""
    <style>
    .article-card {
        background: #12192b;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    .article-card .card-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 14px;
        margin-bottom: 14px;
        display: block;
    }
    .article-card .card-title {
        color: #f8fafc;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0 0 8px 0;
        line-height: 1.4;
    }
    .article-card .card-meta {
        color: #91a0b8;
        font-size: 0.8rem;
        margin: 0 0 10px 0;
    }
    .article-card .ai-label {
        color: #667eea;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 6px 0;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .article-card .card-preview {
        color: #d8dfeb;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    preview = article.get("preview") or "No preview available."

    st.markdown(f"""
    <div class="article-card">
        <img src="{article.get("cover_image", "")}" class="card-img" />
        <div class="card-title">{article.get("title", "Untitled")}</div>
        <div class="card-meta">{format_meta(article)}</div>
        <div class="ai-label">✨ AI Summary</div>
        <div class="card-preview">{preview}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Read more",
        key=f'read_{article["article_id"]}',
        icon=":material/arrow_forward:",
        use_container_width=True
    ):
        st.switch_page(
            "pages/article_details.py",
            query_params={"article_id": str(article["article_id"])}
        )
        st.stop()


def render_news_grid(articles):
    cols = st.columns(3, gap="medium")
    for i, article in enumerate(articles):
        with cols[i % 3]:
            article_card(article)


title_col, actions_col = st.columns([10, 2], vertical_alignment="center")

with title_col:
    st.title("For You")

with actions_col:
    st.markdown('<div class="top-gap"></div>', unsafe_allow_html=True)
    a, b = st.columns(2, gap="small")

    with a:
        if st.button(
            "",
            key="saved_page",
            icon=":material/bookmark:",
            use_container_width=True
        ):
            st.switch_page("pages/saved_articles_page.py")
            st.stop()

    with b:
        if st.button(
            "",
            key="profile_page",
            icon=":material/account_circle:",
            use_container_width=True
        ):
            st.switch_page("pages/profile_page.py")
            st.stop()

articles = api_client.get_news()

if not articles:
    st.info("No articles available.")
else:
    lead_story(articles[0])
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    if len(articles) > 1:
        render_news_grid(articles[1:])