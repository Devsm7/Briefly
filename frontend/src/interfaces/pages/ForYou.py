import streamlit as st
import streamlit.components.v1 as components
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

    .cat-tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }
    .cat-business     { background: #1e3a5f; color: #60a5fa; }
    .cat-sport        { background: #1a3a2a; color: #4ade80; }
    .cat-politics     { background: #3b1f3f; color: #c084fc; }
    .cat-tech         { background: #1a2f3f; color: #38bdf8; }
    .cat-health       { background: #3a2020; color: #f87171; }
    .cat-entertainment{ background: #3a2a10; color: #fb923c; }
    .cat-world        { background: #1e2f40; color: #67e8f9; }
    .cat-environment  { background: #1a3020; color: #86efac; }
    .cat-food         { background: #3a2e10; color: #fde68a; }
    .cat-tourism      { background: #2a1a3a; color: #e879f9; }
    .cat-other        { background: #1e2535; color: #94a3b8; }

    /* Search input */
    div[data-testid="stTextInput"] input {
        background: #12192b !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
        font-size: 1rem !important;
        padding: 0.65rem 1rem !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.25) !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #4a5568 !important;
    }

    /* Floating AI Brief button */
    #ai-brief-float-anchor + div.element-container {
        position: fixed !important;
        bottom: 2rem;
        left: 2rem;
        z-index: 9999;
    }
    #ai-brief-float-anchor + div.element-container button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 22px rgba(102, 126, 234, 0.55) !important;
        min-height: unset !important;
        letter-spacing: 0.02em;
    }
    #ai-brief-float-anchor + div.element-container button:hover {
        box-shadow: 0 6px 30px rgba(102, 126, 234, 0.75) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)


def short_preview(text, limit=200):
    if not text:
        return "No preview available."
    text = str(text).strip()
    return text


def get_preview(article: dict) -> str:
    return article.get("preview") or "No preview available."


def format_meta(article):
    source = article.get("source") or "Unknown source"
    date = article.get("date") or "No date"
    return f"{source} • {date}"


def category_tag(article) -> str:
    cat = (article.get("category") or "other").lower().replace(" ", "")
    label = cat.capitalize()
    css_class = f"cat-{cat}" if cat in {
        "business", "sport", "politics", "tech", "health",
        "entertainment", "world", "environment", "food", "tourism"
    } else "cat-other"
    return f'<span class="cat-tag {css_class}">{label}</span>'


def lead_story(article):
    """Lead story card — image and text in one unified card, side-by-side layout."""
    preview = get_preview(article)
    cover = article.get("cover_image", "")
    title = article.get("title", "Untitled")
    meta = format_meta(article)
    art_id = article["article_id"]

    st.markdown("""
    <style>
    .lead-card {
        background: #12192b;
        border: 1px solid #1e293b;
        border-radius: 22px;
        overflow: hidden;
        display: flex;
    }
    .lead-img-wrap {
        flex: 0 0 45%;
        overflow: hidden;
        border-radius: 14px 0 0 14px;
    }
    .lead-img {
        width: 100%;
        height: 340px;
        object-fit: cover;
        display: block;
        border-radius: 14px 0 0 14px;
    }
    .lead-body {
        flex: 1;
        padding: 24px 28px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .lead-label {
        color: #667eea;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }
    .lead-title {
        color: #f8fafc;
        font-size: 1.5rem;
        font-weight: 800;
        line-height: 1.3;
        margin: 0 0 12px;
    }
    .lead-meta {
        color: #91a0b8;
        font-size: 0.82rem;
        margin-bottom: 14px;
    }
    .lead-preview {
        color: #d8dfeb;
        font-size: 0.95rem;
        line-height: 1.65;
        margin: 0;
    }
    @media (max-width: 700px) {
        .lead-card { flex-direction: column; }
        .lead-img-wrap { flex: none; width: 100%; }
        .lead-img { height: 220px; }
    }
    </style>
    """, unsafe_allow_html=True)

    card_img = f'<img src="{cover}" class="lead-img" loading="lazy" decoding="async" onerror="this.style.display=\'none\'" />' if cover else ""

    st.markdown(f"""
    <div class="lead-card">
        <div class="lead-img-wrap">{card_img}</div>
        <div class="lead-body">
            <div class="lead-label">✨ Top story &nbsp;{category_tag(article)}</div>
            <div class="lead-title">{title}</div>
            <div class="lead-meta">{meta}</div>
            <div class="lead-preview">{preview[:280]}{'…' if len(preview) > 280 else ''}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Read full story", key=f"lead_{art_id}", icon=":material/arrow_forward:", use_container_width=True):
        st.session_state["viewing_article_id"] = art_id
        st.switch_page("pages/article_details.py")
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

    preview = get_preview(article)

    st.markdown(f"""
    <div class="article-card">
        <img src="{article.get("cover_image", "")}" class="card-img" loading="lazy" decoding="async" />
        {category_tag(article)}
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
        st.session_state["viewing_article_id"] = article["article_id"]
        st.switch_page("pages/article_details.py")
        st.stop()


def render_news_grid(articles):
    cols = st.columns(3, gap="medium")
    for i, article in enumerate(articles):
        with cols[i % 3]:
            article_card(article)


@st.dialog("✨ AI News Brief", width="large")
def show_ai_brief():
    # Fetch English summary only once — cache survives radio toggles within the same dialog session
    if "ai_brief_en" not in st.session_state:
        with st.spinner("Generating AI brief…"):
            try:
                st.session_state.ai_brief_en = api_client.get_overall_summary()
            except Exception as e:
                st.error(f"Could not load summary: {e}")
                return

    en_summary = st.session_state.ai_brief_en
    if not en_summary:
        st.info("No summary available yet.")
        return

    lang = st.radio(
        "",
        ["🇬🇧 English", "🇸🇦 العربية"],
        horizontal=True,
        label_visibility="collapsed",
        key="ai_brief_lang",
    )

    if lang == "🇸🇦 العربية":
        # Translate only once — cache survives toggling back and forth
        if "ai_brief_ar" not in st.session_state:
            with st.spinner("Translating to Arabic…"):
                st.session_state.ai_brief_ar = api_client.translate_summary(en_summary)
        ar_text = st.session_state.ai_brief_ar
        if ar_text:
            st.markdown(
                f"<div style='color:#d8dfeb;font-size:1.05rem;line-height:2;"
                f"direction:rtl;text-align:right;font-family:Arial,sans-serif'>{ar_text}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.error("Translation failed — tap English and try Arabic again.")
    else:
        # Use st.markdown so **bold** and other markdown renders natively
        st.markdown(
            f"<style>.brief-en {{color:#d8dfeb;font-size:1rem;line-height:1.8}}"
            f".brief-en b,.brief-en strong{{color:#f8fafc}}</style>",
            unsafe_allow_html=True,
        )
        st.markdown(en_summary)


if st.session_state.pop("_scroll_top", False):
    components.html("""
    <script>
        var el = parent.document.querySelector('[data-testid="stAppViewContainer"]');
        if (el) el.scrollTop = 0;
        parent.window.scrollTo(0, 0);
        parent.document.documentElement.scrollTop = 0;
        parent.document.body.scrollTop = 0;
    </script>
    """, height=0)

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

# ── Search bar ────────────────────────────────────────────────────────────────
search_col, _ = st.columns([3, 1])
with search_col:
    search_query = st.text_input(
        "search",
        placeholder="🔍  Search articles…",
        key="search_input",
        label_visibility="collapsed",
    )

# ── Floating AI Brief button ──────────────────────────────────────────────────
st.markdown('<div id="ai-brief-float-anchor"></div>', unsafe_allow_html=True)
if st.button("✨ AI Brief", key="ai_brief_btn"):
    show_ai_brief()

PER_PAGE = 50

if "news_page" not in st.session_state:
    st.session_state.news_page = 1

# Fetch all ranked articles once and cache; page navigation slices locally
if "recommendations_cache" not in st.session_state:
    with st.spinner("Loading your feed…"):
        response = api_client.get_recommendations(page=1, per_page=300)
        st.session_state.recommendations_cache = response.get("articles", [])

all_articles = st.session_state.recommendations_cache
total = len(all_articles)
total_pages = max((total + PER_PAGE - 1) // PER_PAGE, 1)
current_page = st.session_state.news_page

offset = (current_page - 1) * PER_PAGE
articles = all_articles[offset:offset + PER_PAGE]

if search_query and search_query.strip():
    # ── Search results ────────────────────────────────────────────────────────
    with st.spinner(f'Searching for "{search_query}"…'):
        try:
            results = api_client.search_articles(q=search_query.strip(), limit=30)
        except Exception as e:
            st.error(f"Search failed: {e}")
            results = []
    if results:
        st.markdown(
            f"<p style='color:#91a0b8; font-size:0.9rem; margin-bottom:1rem;'>"
            f"{len(results)} results for <b style='color:#f8fafc'>\"{search_query}\"</b></p>",
            unsafe_allow_html=True,
        )
        render_news_grid(results)
    else:
        st.info(f'No results found for "{search_query}".')

elif not articles:
    st.info("No articles available.")
else:
    # ── Normal feed ───────────────────────────────────────────────────────────
    if current_page == 1:
        lead_story(articles[0])
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        render_news_grid(articles[1:])
    else:
        render_news_grid(articles)

    # Pagination controls
    if total_pages > 1:
        st.markdown("---")
        col_prev, col_info, col_next = st.columns([1, 2, 1], vertical_alignment="center")
        with col_prev:
            if current_page > 1:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.news_page = current_page - 1
                    st.session_state._scroll_top = True
                    st.rerun()
        with col_info:
            st.markdown(
                f"<div style='text-align:center; color:#91a0b8; font-size:0.9rem;'>"
                f"Page {current_page} of {total_pages} &nbsp;|&nbsp; {total} articles"
                f"</div>",
                unsafe_allow_html=True,
            )
        with col_next:
            if current_page < total_pages:
                if st.button("Next →", use_container_width=True):
                    st.session_state.news_page = current_page + 1
                    st.session_state._scroll_top = True
                    st.rerun()